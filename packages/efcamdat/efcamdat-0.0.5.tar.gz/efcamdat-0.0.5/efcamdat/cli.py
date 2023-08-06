from typer import Typer
from os.path import abspath, dirname, join
import xml.etree.ElementTree as ET
import functools
import pydantic
import yaml
import json
import nltk

class EFCAMDATWriting(pydantic.BaseModel):
                written_text: str
                learner_id: str
                learner_nationality: str
                writing_id: str
                writing_level: str
                writing_unit: str 
                topic_id: str
                topic_text: str 
                date_text: str
                grade_text: str

class EFCAMDATSentence(pydantic.BaseModel):
                written_text: str
                sentence_text: str
                learner_id: str
                learner_nationality: str
                writing_id: str
                writing_level: str
                writing_unit: str 
                topic_id: str
                topic_text: str 
                date_text: str
                grade_text: str

app = Typer()

@app.callback()
def callback():
    """
        CLI with some functionalities to process the EFCAMDAT dataset
    """

@app.command()
def from_config(config = None):
    '''
        runs a command from a config a file
    '''
    commands = {
            "rawxmltojson" :rawxmltojson,
            "efcamdatwritingstosentencesjson" : efcamdatwritingstosentencesjson
            }
    if config:
        with open(config) as inpf:
            config_dict = yaml.load(inpf.read(), Loader=yaml.Loader)  
            command = config_dict["command"]
            del config_dict["command"]
            commands[command](**config_dict)
    else:
        print('this command only works with a --config filepath')

@app.command()
def rawxmltojson(filepath: str, output_path: str):
    '''
        given a input XML file and an output_path 
        create a json file in the output path


        expected XML format :
        <?xml version="1.0" encoding="UTF-8"?>\n
        <selection id="935c5512bb451c0c59bf9de64c2d3d88">\n
          <meta>\n
            <title><?xml version="1.0" encoding="UTF-8"?>\n
            <url>https://philarion.mml.cam.ac.uk/efcamdat/</url>\n
          </meta>
          <writings>
            <writing id="1" level="6" unit="1">
              <learner id="103510" nationality="no"/>
              <topic id="41">Writing a movie plot</topic>
              <date>2011-03-20 12:44:16.790</date>
              <grade>90</grade>
            <text>
              After some time, the affection between them is progressing well. John's personality deeply moved Isabella. So Isabella decided to break up with Tom and fell in love with John. John also feeled that Isabella was the woman he loved deeply. To his joy, he could find his true love during his travel. In the end, they married together.
            </text>
            </writing>
            <writing id="2" level="6" unit="2">
                ...
            </writing>
            ...
            <writing>
            </writing>
    '''
    with open(filepath) as inpf:
        edits = { 
                    '<br>':'',
                    '<code>': '',
                    '</code>':'',
                    '\t':''
                   }
        content = inpf.read()
        for k, v in edits.items():
            content = content.replace(k, v)

        root = ET.fromstring(content)
        meta, writings = [children for children in root] 
        writings_dict = {"writings":[]}
        for writing in writings:
            learner, topic, date, grade, text = [children for children in writing]
            w = dict(writing.items()) # writing inside tag data
            writing_id, writing_level, writing_unit = w["id"], w["level"], w["unit"] 
            l = dict(learner.items()) # learner inside tag data
            learner_id, learner_nationality = l['id'],l['nationality']
            topic_id, topic_text = dict(topic.items())['id'], topic.text
            date_text = date.text
            grade_text = grade.text
            written_text = text.text.replace("\n","").replace("\t","").strip()
            # sentences = sent_tokenize(written_text) 
            writing = EFCAMDATWriting(**{
                    "written_text" : written_text,
                    "learner_id": learner_id,
                    "learner_nationality": learner_nationality,
                    "writing_id" :writing_id,
                    "writing_level" :writing_level,
                    "writing_unit" : writing_unit, 
                    "topic_id": topic_id,
                    "topic_text": topic_text, 
                    "date_text" : date_text,
                    "grade_text" : grade_text
                    })
            writings_dict["writings"].append(writing.dict())
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(writings_dict, f, ensure_ascii=False, indent=4)

@app.command()
def efcamdatwritingstosentencesjson(filepath: str, output_path: str):
    '''
        given a json file path of format :
        { "writings": [ EFCAMDATWriting ] }
        for each writing create a duplicate object but with a "sentence" property
    '''
    with open(filepath) as inpf:
        writings_dict = json.load(inpf)
        sentences_dict = {"sentences": []}
        for writing in writings_dict["writings"]:
            for sentence in nltk.sent_tokenize(writing["written_text"]):
                sentence_obj = EFCAMDATSentence(**{
                        **writing,
                        "sentence_text": sentence
                    })
                sentences_dict["sentences"].append(sentence_obj.dict())
    with open(output_path, "w") as outf:
        json.dump(sentences_dict, outf, ensure_ascii=False, indent=4)

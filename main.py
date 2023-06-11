from reactpy import web,html,component,use_state
from reactpy.backend.fastapi import configure
from fastapi import FastAPI
from dataclasses import dataclass
import random
# NOW CREATE dataclass
@dataclass
class Person:
    myid:int
    name:str
    age:int


app = FastAPI()
@component
def Mycrud():
    # CREATE STATE
    persons = use_state([])
    nametxt , set_nametxt = use_state("")
    agetxt , set_agetxt = use_state(0)

    nameupdate,set_nameupdate = use_state("")
    ageupdate,set_ageupdate = use_state("")
    selectid = use_state(0)



    def addnew(event):
        newperson = Person(random.randint(0,400),nametxt,agetxt)
        persons.set_value(persons.value + [newperson])
        print(persons)
    def editbtn(b):
        for x in persons.value:
            if x.myid == b:
                set_nameupdate(x.name)
                set_ageupdate(x.age)
                selectid.set_value(x.myid)





    def deletebtn(myid):
        updated_persons = [person for person in persons.value if person.myid != myid]
        # AND UPDATE persons
        persons.set_value(updated_persons)    

    def updatebtn(event):
        myeditdata = persons.value.copy()
        for x in persons.value:
            # NOW IF FOUND THEN CHANGE YOU SELECT DATA
            if x.myid == selectid.value:
                print(myeditdata)
                x.name = nameupdate
                x.age = ageupdate
                x.myid = selectid.value
        # AND CLEAR INPUT
        set_nameupdate("")
        set_ageupdate("")
        selectid.set_value(0)





    return html.div(
        html.h1("Mycrud"),
        # NOW CREATE INPUT NAME AND AGE
        html.input({
            "type":"text",
            "placeholder":"name here",
            "on_change":lambda event:set_nametxt(event['target']['value'])

            }),
        html.input({
            "type":"text",
            "placeholder":"age here",
            "on_change":lambda event:set_agetxt(event['target']['value'])

            }),
        html.button({
            "on_click":addnew
            },"add new now"),

        # NOW CREATE TABLE
        html.table(
            html.thead(
                html.tr(
                    html.th("Name"),
                    html.th("age")
                    )
                ),
            html.tbody(
                # NOW LOOP FROM dataclass
                [html.tr(
                    html.td(person.name),
                    html.td(person.age),
                # AND CREATE EDIT AND DELETE BUTTON
                html.button({
                    "on_click":lambda event,index=person.myid:editbtn(index)
                    },"edit"),
                 html.button({
                    "on_click":lambda event,index=person.myid:deletebtn(index)
                    },"delete"),

                    )for person in persons.value]
                )
            ),
        # THIS FOR INPUT UPDATE
        html.input({
            "type":"text",
            "placeholder":"name Update here",
            "value":nameupdate,
            "on_change":lambda event:set_nameupdate(event['target']['value'])

            }),
        html.input({
            "type":"text",
            "placeholder":"age Update here",
             "value":ageupdate,
            "on_change":lambda event:set_ageupdate(event['target']['value'])

            }),
        html.button({
            "on_click":updatebtn
            },"You update now")

        )

configure(app,Mycrud)
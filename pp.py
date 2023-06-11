from reactpy import html, web, component, use_state
from reactpy.backend.fastapi import configure
from fastapi import FastAPI
from dataclasses import dataclass
import random
import copy

@dataclass
class Person:
    myid:int
    name: str
    age: int

app = FastAPI()

@component
def mycrudapp():
    persons = use_state([])
    nametxt,set_nametxt = use_state("")
    agetxt,set_agetxt = use_state(0)
    selectid = use_state(0)

    nameupdate,set_nameupdate = use_state("")
    ageupdate,set_ageupdate = use_state(0)


    def addnew(event):
        newperson = Person(random.randint(0,100),nametxt, agetxt)
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
        persons.set_value(updated_persons)

    def updatebtn(event):
        myeditdata = persons.value.copy()
        for x in persons.value:
            if x.myid == selectid.value:
                print(myeditdata)
                x.name = nameupdate
                x.age = ageupdate
                x.myid = selectid.value
        set_nameupdate("")
        set_ageupdate(0)
        selectid.set_value(0)



    return html.div(
        html.h1("hai"),
        html.input({
            "type":"text",
            "placeholder":"inser name",
            "on_change":lambda event:set_nametxt(event['target']['value'])
            }),
        html.input({
            "type":"text",
            "placeholder":"inser age",
            "on_change":lambda event:set_agetxt(event['target']['value'])
            }),

        html.button({
            "on_click": addnew
        }, "add new"),
        html.table(
            html.thead(
                html.tr(
                    html.th("Name"),
                    html.th("Age"),
                    html.th("Actions"),
                ),
            ),
            html.tbody(
                [html.tr(

                html.td(person.name),
                html.td(person.age),
                html.button({
                    "on_click":lambda event,index=person.myid:editbtn(index)
                    },"edit"),
                html.button({
                    "on_click":lambda event,index=person.myid:deletebtn(index)
                    },"delete")
                ) for person in persons.value]  # Mengakses nilai aktual persons sebelum iterasi
            )
        ),

        # UPDATE
        html.input({
            "type":"text",
            "value":nameupdate,
            "placeholder":"update name",
            "on_change":lambda event:set_nameupdate(event['target']['value'])
            }),
        html.input({
            "type":"text",
            "value":ageupdate,
            "placeholder":"update age",
            "on_change":lambda event:set_ageupdate(event['target']['value'])
            }),
        html.button({
            "on_click":updatebtn
            },"update now")
    )

configure(app, mycrudapp)

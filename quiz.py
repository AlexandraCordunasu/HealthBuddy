import kivy
from kivy.app import App
from kivy.uix.label import Label

last_name = input("Vă rog să introduceți numele dumneavoastra:")
first_name = input("Vă rog să introduceți prenumele dumneavostra:")
age = input("Ce vârstă aveți?")
height = input("Ce înălțime aveți?")
weight = input("Câte kilograme aveți?")
QUESTIONS = {
    "Sex M/F": [
        "masculin", "Feminin", "Prefer să nu spun"],
    "Cat de activ sunteți?": [
        "Stil de viață sedentar", "Activitate fizică medie", "Activitate fizică moderată", "Activitate fizică intensă-specifică antrenorilor și sportivilor"
    ],
    "Ce ideal aveți?": [
        "Slăbit","Luare in greutate","Mentinere"
    ],
    "Ce ati dori sa lucrati mai mult?" :[
        "Gambe","Coapse","Fesieri","Picioare","Abdomen","Piept","Spate","Biceps","Triceps","Umeri","Brate","Picioare"
    ],
    "Cate minute faceti sport pe zi?" : [
    "0 minute", "30 minute","45 minute","60 minute", "90 minute","120 minute","150 min","190 minute"
    ],
}
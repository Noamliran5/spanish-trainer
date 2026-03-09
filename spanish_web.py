#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import random
from flask import Flask, jsonify, request, session, render_template_string, redirect, url_for

app = Flask(__name__)
app.secret_key = "multilang-trainer-secret-2024"

# ── Sentence databases ─────────────────────────────────────────────────────────

SENTENCES = {
    "spanish": [
        # ברכות ונימוסים
        ("Buenos días",                       "בוקר טוב"),
        ("Buenas tardes",                     "אחר הצהריים טובים"),
        ("Buenas noches",                     "לילה טוב"),
        ("Hola",                              "שלום"),
        ("Adiós",                             "להתראות"),
        ("Hasta luego",                       "להתראות"),
        ("Hasta mañana",                      "להתראות מחר"),
        ("Hasta pronto",                      "נתראה בקרוב"),
        ("Mucho gusto",                       "נעים להכיר"),
        ("Encantado",                         "שמח להכיר"),
        ("Por favor",                         "בבקשה"),
        ("Gracias",                           "תודה"),
        ("Muchas gracias",                    "תודה רבה"),
        ("De nada",                           "על לא דבר"),
        ("Lo siento",                         "אני מצטער"),
        ("Perdón",                            "סליחה"),
        ("Con permiso",                       "בסליחה"),
        ("Salud",                             "לבריאות"),
        ("Feliz cumpleaños",                  "יום הולדת שמח"),
        ("Feliz año nuevo",                   "שנה טובה"),
        # היכרות
        ("¿Cómo estás?",                     "מה שלומך?"),
        ("Estoy bien, gracias",               "אני בסדר, תודה"),
        ("Estoy muy bien",                    "אני מאוד בסדר"),
        ("Más o menos",                       "כך כך"),
        ("Me llamo Juan",                     "שמי חואן"),
        ("¿Cómo te llamas?",                 "מה שמך?"),
        ("¿Cuántos años tienes?",            "בן כמה אתה?"),
        ("Tengo veinte años",                 "אני בן עשרים"),
        ("¿De dónde eres?",                  "מאיפה אתה?"),
        ("Soy de Israel",                     "אני מישראל"),
        ("¿Dónde vives?",                    "איפה אתה גר?"),
        ("Vivo en Tel Aviv",                  "אני גר בתל אביב"),
        ("¿En qué trabajas?",                "במה אתה עובד?"),
        ("Soy estudiante",                    "אני סטודנט"),
        ("Soy médico",                        "אני רופא"),
        ("Soy maestro",                       "אני מורה"),
        ("Tengo una familia grande",          "יש לי משפחה גדולה"),
        ("Tengo dos hermanos",                "יש לי שני אחים"),
        ("Soy hijo único",                    "אני בן יחיד"),
        # שפה
        ("¿Hablas español?",                 "האם אתה מדבר ספרדית?"),
        ("Sí, un poco",                      "כן, קצת"),
        ("No hablo español",                  "אני לא מדבר ספרדית"),
        ("No entiendo",                       "אני לא מבין"),
        ("¿Puedes repetir?",                 "אתה יכול לחזור?"),
        ("Habla más despacio",                "דבר לאט יותר"),
        ("No sé",                            "אני לא יודע"),
        ("¿Cómo se dice en español?",        "איך אומרים זאת בספרדית?"),
        ("¿Qué significa esto?",             "מה זה אומר?"),
        ("Estoy aprendiendo español",         "אני לומד ספרדית"),
        ("El español es difícil",             "ספרדית קשה"),
        ("El español es fácil",               "ספרדית קלה"),
        # מספרים וזמן
        ("¿Qué hora es?",                    "מה השעה?"),
        ("Son las tres",                      "השעה שלוש"),
        ("Son las ocho de la mañana",         "השעה שמונה בבוקר"),
        ("¿Qué día es hoy?",                 "איזה יום היום?"),
        ("Hoy es lunes",                      "היום יום שני"),
        ("Hoy es viernes",                    "היום יום שישי"),
        ("¿Cuál es la fecha de hoy?",        "מה התאריך היום?"),
        ("Hoy es el primero de enero",        "היום הראשון לינואר"),
        ("Mañana es el examen",               "מחר הוא הבחינה"),
        ("Ayer fui al mercado",               "אתמול הלכתי לשוק"),
        # מזג אוויר
        ("¿Qué tiempo hace?",                "מה מזג האוויר?"),
        ("Hace calor hoy",                    "חם היום"),
        ("Hace frío",                         "קר"),
        ("Está lloviendo",                    "יורד גשם"),
        ("Hace sol",                          "יש שמש"),
        ("Hace viento",                       "יש רוח"),
        ("El tiempo es bueno",                "מזג האוויר טוב"),
        ("El tiempo es malo",                 "מזג האוויר רע"),
        ("Está nublado",                      "מעונן"),
        # מסעדה וקניות
        ("¿Cuánto cuesta?",                  "כמה זה עולה?"),
        ("La cuenta, por favor",              "את החשבון, בבקשה"),
        ("Quiero agua",                       "אני רוצה מים"),
        ("Quiero comer",                      "אני רוצה לאכול"),
        ("Tengo hambre",                      "אני רעב"),
        ("Tengo sed",                         "אני צמא"),
        ("¿Tiene una mesa libre?",           "יש לכם שולחן פנוי?"),
        ("Una mesa para dos",                 "שולחן לשניים"),
        ("La carta, por favor",               "את התפריט, בבקשה"),
        ("¿Qué recomienda?",                 "מה אתה ממליץ?"),
        ("Quiero el pollo",                   "אני רוצה את העוף"),
        ("Sin cebolla, por favor",            "בלי בצל, בבקשה"),
        ("Está muy rico",                     "זה מאוד טעים"),
        ("La comida está fría",               "האוכל קר"),
        ("¿Dónde está el supermercado?",     "איפה הסופרמרקט?"),
        ("¿Tienen descuento?",               "יש לכם הנחה?"),
        ("Es muy caro",                       "זה מאוד יקר"),
        ("Es barato",                         "זה זול"),
        ("¿Puedo pagar con tarjeta?",        "אני יכול לשלם בכרטיס?"),
        ("Me lo llevo",                       "אני לוקח את זה"),
        # כיוונים ותחבורה
        ("¿Dónde está el baño?",            "איפה השירותים?"),
        ("¿Dónde está el hospital?",         "איפה בית החולים?"),
        ("¿Cómo llego al centro?",           "איך מגיעים למרכז?"),
        ("Gira a la derecha",                 "פנה ימינה"),
        ("Gira a la izquierda",               "פנה שמאלה"),
        ("Sigue recto",                       "המשך ישר"),
        ("Está cerca",                        "זה קרוב"),
        ("Está lejos",                        "זה רחוק"),
        ("¿Dónde está la parada del bus?",   "איפה תחנת האוטובוס?"),
        ("Quiero un billete para Madrid",     "אני רוצה כרטיס למדריד"),
        ("¿A qué hora sale el tren?",        "באיזו שעה יוצא הרכבת?"),
        ("He perdido mi maleta",              "אבדתי את המזוודה שלי"),
        # בריאות
        ("Me duele la cabeza",                "כואב לי הראש"),
        ("Me duele el estómago",              "כואב לי הבטן"),
        ("Estoy enfermo",                     "אני חולה"),
        ("Necesito un médico",                "אני צריך רופא"),
        ("Tengo fiebre",                      "יש לי חום"),
        ("Soy alérgico a la penicilina",      "אני אלרגי לפניצילין"),
        ("¿Dónde está la farmacia?",         "איפה בית המרקחת?"),
        ("Necesito estas pastillas",          "אני צריך את הכדורים האלה"),
        ("Llame a una ambulancia",            "תקרא לאמבולנס"),
        # רגשות ודעות
        ("Estoy feliz",                       "אני שמח"),
        ("Estoy triste",                      "אני עצוב"),
        ("Estoy cansado",                     "אני עייף"),
        ("Estoy aburrido",                    "אני משועמם"),
        ("Estoy nervioso",                    "אני עצבני"),
        ("Estoy emocionado",                  "אני נרגש"),
        ("Me gusta mucho",                    "אני מאוד אוהב את זה"),
        ("No me gusta",                       "אני לא אוהב את זה"),
        ("Es muy interesante",                "זה מאוד מעניין"),
        ("Es muy aburrido",                   "זה מאוד משעמם"),
        ("Tienes razón",                      "אתה צודק"),
        ("No tienes razón",                   "אתה לא צודק"),
        ("Estoy de acuerdo",                  "אני מסכים"),
        ("No estoy de acuerdo",               "אני לא מסכים"),
        ("Me parece bien",                    "זה נראה לי בסדר"),
        ("Es una buena idea",                 "זו רעיון טוב"),
        # בית ומשפחה
        ("Vivo en un apartamento",            "אני גר בדירה"),
        ("Mi casa es grande",                 "הבית שלי גדול"),
        ("Tengo dos habitaciones",            "יש לי שני חדרים"),
        ("¿Cuántas personas viven aquí?",    "כמה אנשים גרים כאן?"),
        ("Mi madre es profesora",             "אמא שלי היא מורה"),
        ("Mi padre trabaja mucho",            "אבא שלי עובד הרבה"),
        ("Mi hermana es mayor que yo",        "האחות שלי גדולה ממני"),
        ("Tengo un perro",                    "יש לי כלב"),
        ("El gato es muy bonito",             "החתול מאוד יפה"),
        # לימודים ועבודה
        ("Estudio en la universidad",         "אני לומד באוניברסיטה"),
        ("Tengo clases por la mañana",        "יש לי שיעורים בבוקר"),
        ("El libro es interesante",           "הספר מעניין"),
        ("Necesito estudiar más",             "אני צריך ללמוד יותר"),
        ("El examen fue difícil",             "הבחינה הייתה קשה"),
        ("Saqué una buena nota",              "קיבלתי ציון טוב"),
        ("Trabajo en una empresa",            "אני עובד בחברה"),
        ("Tengo una reunión importante",      "יש לי פגישה חשובה"),
        ("El jefe es muy estricto",           "הבוס מאוד קפדן"),
        ("Gano buen sueldo",                  "אני מרוויח משכורת טובה"),
        # פנאי ובילוי
        ("¿Qué haces en tu tiempo libre?",   "מה אתה עושה בזמן הפנוי?"),
        ("Me gusta leer",                     "אני אוהב לקרוא"),
        ("Me gusta escuchar música",          "אני אוהב להאזין למוזיקה"),
        ("Vamos al cine esta noche",          "בואו נלך לקולנוע הלילה"),
        ("La película fue muy buena",         "הסרט היה מאוד טוב"),
        ("¿A qué hora empieza?",             "באיזו שעה זה מתחיל?"),
        ("Vamos a la playa",                  "בואו נלך לחוף הים"),
        ("El mar está muy frío",              "הים מאוד קר"),
        ("¿Quieres jugar al fútbol?",        "אתה רוצה לשחק כדורגל?"),
        ("Hago deporte todos los días",       "אני עושה ספורט כל יום"),
        ("Me encanta bailar",                 "אני מאוד אוהב לרקוד"),
        ("¿Quieres salir esta noche?",       "אתה רוצה לצאת הלילה?"),
        # טכנולוגיה
        ("¿Tienes teléfono móvil?",          "יש לך טלפון נייד?"),
        ("Se me ha roto el móvil",            "הטלפון שלי התקלקל"),
        ("¿Puedo usar tu cargador?",         "אני יכול להשתמש בטוען שלך?"),
        ("¿Cuál es la contraseña del wifi?", "מה הסיסמה של הוויפי?"),
        ("Mándame un mensaje",                "שלח לי הודעה"),
        ("¿Tienes WhatsApp?",                "יש לך ווטסאפ?"),
        ("El ordenador no funciona",          "המחשב לא עובד"),
        ("Necesito imprimir esto",            "אני צריך להדפיס את זה"),
        # שאלות כלליות
        ("¿Qué tal?",                        "מה נשמע?"),
        ("¿Qué pasa?",                       "מה קורה?"),
        ("¿Por qué?",                        "למה?"),
        ("¿Cuándo?",                         "מתי?"),
        ("¿Quién es?",                       "מי זה?"),
        ("¿Qué quieres?",                    "מה אתה רוצה?"),
        ("¿Adónde vas?",                     "לאן אתה הולך?"),
        ("¿Qué comes?",                      "מה אתה אוכל?"),
        ("¿Qué piensas?",                    "מה אתה חושב?"),
        ("¿Cómo fue tu día?",               "איך היה היום שלך?"),
        # ביטויים שימושיים
        ("Necesito ayuda",                    "אני צריך עזרה"),
        ("Llama a la policía",                "תקרא למשטרה"),
        ("¡Cuidado!",                        "זהירות!"),
        ("¡Espera un momento!",              "רגע אחד!"),
        ("No hay problema",                   "אין בעיה"),
        ("Claro que sí",                      "כמובן שכן"),
        ("Por supuesto",                      "כמובן"),
        ("A veces",                           "לפעמים"),
        ("Siempre",                           "תמיד"),
        ("Nunca",                             "אף פעם"),
        ("Ya voy",                            "אני כבר בא"),
        ("Ahora mismo",                       "עכשיו ממש"),
        ("Más tarde",                         "מאוחר יותר"),
        ("Te quiero",                         "אני אוהב אותך"),
        ("Todo está bien",                    "הכל בסדר"),
        ("Me llevo bien con todos",           "אני מסתדר טוב עם כולם"),
        ("Tengo muchos amigos",               "יש לי הרבה חברים"),
        ("La música me relaja",               "המוזיקה מרגיעה אותי"),
    ],

    "english": [
        # ברכות ונימוסים
        ("Good morning",                      "בוקר טוב"),
        ("Good afternoon",                    "אחר הצהריים טובים"),
        ("Good evening",                      "ערב טוב"),
        ("Good night",                        "לילה טוב"),
        ("Hello",                             "שלום"),
        ("Hi",                                "היי"),
        ("Goodbye",                           "להתראות"),
        ("See you later",                     "נתראה אחר כך"),
        ("See you tomorrow",                  "נתראה מחר"),
        ("Nice to meet you",                  "נעים להכיר אותך"),
        ("Please",                            "בבקשה"),
        ("Thank you",                         "תודה"),
        ("Thank you very much",               "תודה רבה"),
        ("You're welcome",                    "על לא דבר"),
        ("I'm sorry",                         "אני מצטער"),
        ("Excuse me",                         "סליחה"),
        ("Cheers",                            "לחיים"),
        ("Happy birthday",                    "יום הולדת שמח"),
        ("Happy new year",                    "שנה טובה"),
        # היכרות
        ("How are you?",                      "מה שלומך?"),
        ("I'm fine, thank you",               "אני בסדר, תודה"),
        ("I'm very well",                     "אני מאוד בסדר"),
        ("So so",                             "כך כך"),
        ("My name is David",                  "שמי דוד"),
        ("What is your name?",                "מה שמך?"),
        ("How old are you?",                  "בן כמה אתה?"),
        ("I am twenty years old",             "אני בן עשרים"),
        ("Where are you from?",               "מאיפה אתה?"),
        ("I am from Israel",                  "אני מישראל"),
        ("Where do you live?",                "איפה אתה גר?"),
        ("I live in Tel Aviv",                "אני גר בתל אביב"),
        ("What do you do for work?",          "במה אתה עובד?"),
        ("I am a student",                    "אני סטודנט"),
        ("I am a doctor",                     "אני רופא"),
        ("I am a teacher",                    "אני מורה"),
        ("I have a big family",               "יש לי משפחה גדולה"),
        ("I have two brothers",               "יש לי שני אחים"),
        ("I am an only child",                "אני בן יחיד"),
        # שפה
        ("Do you speak English?",             "האם אתה מדבר אנגלית?"),
        ("Yes, a little",                     "כן, קצת"),
        ("I don't speak English",             "אני לא מדבר אנגלית"),
        ("I don't understand",                "אני לא מבין"),
        ("Can you repeat that?",              "אתה יכול לחזור על זה?"),
        ("Please speak more slowly",          "דבר לאט יותר, בבקשה"),
        ("I don't know",                      "אני לא יודע"),
        ("How do you say this in English?",   "איך אומרים זאת באנגלית?"),
        ("What does this mean?",              "מה זה אומר?"),
        ("I am learning English",             "אני לומד אנגלית"),
        ("English is difficult",              "אנגלית קשה"),
        ("English is easy",                   "אנגלית קלה"),
        # זמן
        ("What time is it?",                  "מה השעה?"),
        ("It is three o'clock",               "השעה שלוש"),
        ("It is eight in the morning",        "השעה שמונה בבוקר"),
        ("What day is it today?",             "איזה יום היום?"),
        ("Today is Monday",                   "היום יום שני"),
        ("Today is Friday",                   "היום יום שישי"),
        ("What is today's date?",             "מה התאריך היום?"),
        ("Today is the first of January",     "היום הראשון לינואר"),
        ("The exam is tomorrow",              "הבחינה היא מחר"),
        ("I went to the market yesterday",    "הלכתי לשוק אתמול"),
        # מזג אוויר
        ("What is the weather like?",         "מה מזג האוויר?"),
        ("It is hot today",                   "חם היום"),
        ("It is cold",                        "קר"),
        ("It is raining",                     "יורד גשם"),
        ("It is sunny",                       "יש שמש"),
        ("It is windy",                       "יש רוח"),
        ("The weather is nice",               "מזג האוויר נחמד"),
        ("The weather is bad",                "מזג האוויר רע"),
        ("It is cloudy",                      "מעונן"),
        # מסעדה וקניות
        ("How much does it cost?",            "כמה זה עולה?"),
        ("The bill, please",                  "את החשבון, בבקשה"),
        ("I want water",                      "אני רוצה מים"),
        ("I want to eat",                     "אני רוצה לאכול"),
        ("I am hungry",                       "אני רעב"),
        ("I am thirsty",                      "אני צמא"),
        ("Do you have a free table?",         "יש לכם שולחן פנוי?"),
        ("A table for two",                   "שולחן לשניים"),
        ("The menu, please",                  "את התפריט, בבקשה"),
        ("What do you recommend?",            "מה אתה ממליץ?"),
        ("I want the chicken",                "אני רוצה את העוף"),
        ("Without onion, please",             "בלי בצל, בבקשה"),
        ("It is very delicious",              "זה מאוד טעים"),
        ("The food is cold",                  "האוכל קר"),
        ("Where is the supermarket?",         "איפה הסופרמרקט?"),
        ("Do you have a discount?",           "יש לכם הנחה?"),
        ("It is very expensive",              "זה מאוד יקר"),
        ("It is cheap",                       "זה זול"),
        ("Can I pay by card?",                "אני יכול לשלם בכרטיס?"),
        ("I will take it",                    "אני לוקח את זה"),
        # כיוונים ותחבורה
        ("Where is the bathroom?",            "איפה השירותים?"),
        ("Where is the hospital?",            "איפה בית החולים?"),
        ("How do I get to the center?",       "איך מגיעים למרכז?"),
        ("Turn right",                        "פנה ימינה"),
        ("Turn left",                         "פנה שמאלה"),
        ("Go straight",                       "המשך ישר"),
        ("It is close",                       "זה קרוב"),
        ("It is far",                         "זה רחוק"),
        ("Where is the bus stop?",            "איפה תחנת האוטובוס?"),
        ("I want a ticket to London",         "אני רוצה כרטיס ללונדון"),
        ("What time does the train leave?",   "באיזו שעה יוצא הרכבת?"),
        ("I lost my suitcase",                "אבדתי את המזוודה שלי"),
        # בריאות
        ("My head hurts",                     "כואב לי הראש"),
        ("My stomach hurts",                  "כואב לי הבטן"),
        ("I am sick",                         "אני חולה"),
        ("I need a doctor",                   "אני צריך רופא"),
        ("I have a fever",                    "יש לי חום"),
        ("I am allergic to penicillin",       "אני אלרגי לפניצילין"),
        ("Where is the pharmacy?",            "איפה בית המרקחת?"),
        ("I need these pills",                "אני צריך את הכדורים האלה"),
        ("Call an ambulance",                 "תקרא לאמבולנס"),
        # רגשות
        ("I am happy",                        "אני שמח"),
        ("I am sad",                          "אני עצוב"),
        ("I am tired",                        "אני עייף"),
        ("I am bored",                        "אני משועמם"),
        ("I am nervous",                      "אני עצבני"),
        ("I am excited",                      "אני נרגש"),
        ("I really like it",                  "אני מאוד אוהב את זה"),
        ("I don't like it",                   "אני לא אוהב את זה"),
        ("It is very interesting",            "זה מאוד מעניין"),
        ("You are right",                     "אתה צודק"),
        ("You are wrong",                     "אתה לא צודק"),
        ("I agree",                           "אני מסכים"),
        ("I disagree",                        "אני לא מסכים"),
        ("That seems fine to me",             "זה נראה לי בסדר"),
        ("It is a good idea",                 "זו רעיון טוב"),
        # בית ומשפחה
        ("I live in an apartment",            "אני גר בדירה"),
        ("My house is big",                   "הבית שלי גדול"),
        ("I have two rooms",                  "יש לי שני חדרים"),
        ("How many people live here?",        "כמה אנשים גרים כאן?"),
        ("My mother is a teacher",            "אמא שלי היא מורה"),
        ("My father works a lot",             "אבא שלי עובד הרבה"),
        ("My sister is older than me",        "האחות שלי גדולה ממני"),
        ("I have a dog",                      "יש לי כלב"),
        ("The cat is very cute",              "החתול מאוד חמוד"),
        # לימודים ועבודה
        ("I study at university",             "אני לומד באוניברסיטה"),
        ("I have classes in the morning",     "יש לי שיעורים בבוקר"),
        ("The book is interesting",           "הספר מעניין"),
        ("I need to study more",              "אני צריך ללמוד יותר"),
        ("The exam was difficult",            "הבחינה הייתה קשה"),
        ("I got a good grade",                "קיבלתי ציון טוב"),
        ("I work at a company",               "אני עובד בחברה"),
        ("I have an important meeting",       "יש לי פגישה חשובה"),
        ("The boss is very strict",           "הבוס מאוד קפדן"),
        ("I earn a good salary",              "אני מרוויח משכורת טובה"),
        # פנאי
        ("What do you do in your free time?", "מה אתה עושה בזמן הפנוי?"),
        ("I like to read",                    "אני אוהב לקרוא"),
        ("I like to listen to music",         "אני אוהב להאזין למוזיקה"),
        ("Let's go to the cinema tonight",    "בואו נלך לקולנוע הלילה"),
        ("The movie was very good",           "הסרט היה מאוד טוב"),
        ("What time does it start?",          "באיזו שעה זה מתחיל?"),
        ("Let's go to the beach",             "בואו נלך לחוף הים"),
        ("The sea is very cold",              "הים מאוד קר"),
        ("Do you want to play football?",     "אתה רוצה לשחק כדורגל?"),
        ("I exercise every day",              "אני עושה ספורט כל יום"),
        ("I love to dance",                   "אני מאוד אוהב לרקוד"),
        ("Do you want to go out tonight?",    "אתה רוצה לצאת הלילה?"),
        # טכנולוגיה
        ("Do you have a mobile phone?",       "יש לך טלפון נייד?"),
        ("My phone broke",                    "הטלפון שלי התקלקל"),
        ("Can I use your charger?",           "אני יכול להשתמש בטוען שלך?"),
        ("What is the wifi password?",        "מה הסיסמה של הוויפי?"),
        ("Send me a message",                 "שלח לי הודעה"),
        ("Do you have WhatsApp?",             "יש לך ווטסאפ?"),
        ("The computer is not working",       "המחשב לא עובד"),
        ("I need to print this",              "אני צריך להדפיס את זה"),
        # כלליות
        ("What's up?",                        "מה נשמע?"),
        ("What is happening?",                "מה קורה?"),
        ("Why?",                              "למה?"),
        ("When?",                             "מתי?"),
        ("Who is it?",                        "מי זה?"),
        ("What do you want?",                 "מה אתה רוצה?"),
        ("Where are you going?",              "לאן אתה הולך?"),
        ("What are you eating?",              "מה אתה אוכל?"),
        ("What do you think?",                "מה אתה חושב?"),
        ("How was your day?",                 "איך היה היום שלך?"),
        ("I need help",                       "אני צריך עזרה"),
        ("Call the police",                   "תקרא למשטרה"),
        ("Be careful!",                       "זהירות!"),
        ("Wait a moment!",                    "רגע אחד!"),
        ("No problem",                        "אין בעיה"),
        ("Of course",                         "כמובן"),
        ("Sometimes",                         "לפעמים"),
        ("Always",                            "תמיד"),
        ("Never",                             "אף פעם"),
        ("I'm coming",                        "אני בא"),
        ("Right now",                         "עכשיו ממש"),
        ("Later",                             "מאוחר יותר"),
        ("I love you",                        "אני אוהב אותך"),
        ("Everything is fine",                "הכל בסדר"),
        ("I get along with everyone",         "אני מסתדר טוב עם כולם"),
        ("I have many friends",               "יש לי הרבה חברים"),
        ("Music relaxes me",                  "המוזיקה מרגיעה אותי"),
    ],

    "romanian": [
        # ברכות ונימוסים
        ("Bună dimineața",                    "בוקר טוב"),
        ("Bună ziua",                         "יום טוב"),
        ("Bună seara",                        "ערב טוב"),
        ("Noapte bună",                       "לילה טוב"),
        ("Salut",                             "שלום"),
        ("La revedere",                       "להתראות"),
        ("Pe curând",                         "נתראה בקרוב"),
        ("Pe mâine",                          "להתראות מחר"),
        ("Îmi pare bine",                     "נעים להכיר"),
        ("Te rog",                            "בבקשה"),
        ("Mulțumesc",                         "תודה"),
        ("Mulțumesc frumos",                  "תודה רבה"),
        ("Cu plăcere",                        "על לא דבר"),
        ("Îmi pare rău",                      "אני מצטער"),
        ("Scuze",                             "סליחה"),
        ("Noroc",                             "לחיים"),
        ("La mulți ani",                      "יום הולדת שמח"),
        ("Un an nou fericit",                 "שנה טובה"),
        # היכרות
        ("Ce mai faci?",                      "מה שלומך?"),
        ("Sunt bine, mulțumesc",              "אני בסדר, תודה"),
        ("Sunt foarte bine",                  "אני מאוד בסדר"),
        ("Așa și-așa",                        "כך כך"),
        ("Mă numesc Ion",                     "שמי יון"),
        ("Cum te cheamă?",                    "מה שמך?"),
        ("Câți ani ai?",                      "בן כמה אתה?"),
        ("Am douăzeci de ani",                "אני בן עשרים"),
        ("De unde ești?",                     "מאיפה אתה?"),
        ("Sunt din Israel",                   "אני מישראל"),
        ("Unde locuiești?",                   "איפה אתה גר?"),
        ("Locuiesc în Tel Aviv",              "אני גר בתל אביב"),
        ("Cu ce te ocupi?",                   "במה אתה עובד?"),
        ("Sunt student",                      "אני סטודנט"),
        ("Sunt medic",                        "אני רופא"),
        ("Sunt profesor",                     "אני מורה"),
        ("Am o familie mare",                 "יש לי משפחה גדולה"),
        ("Am doi frați",                      "יש לי שני אחים"),
        ("Sunt copil unic",                   "אני בן יחיד"),
        # שפה
        ("Vorbești română?",                  "האם אתה מדבר רומנית?"),
        ("Da, puțin",                         "כן, קצת"),
        ("Nu vorbesc română",                 "אני לא מדבר רומנית"),
        ("Nu înțeleg",                        "אני לא מבין"),
        ("Poți să repeți?",                   "אתה יכול לחזור?"),
        ("Vorbește mai rar",                  "דבר לאט יותר"),
        ("Nu știu",                           "אני לא יודע"),
        ("Cum se spune în română?",           "איך אומרים זאת ברומנית?"),
        ("Ce înseamnă asta?",                 "מה זה אומר?"),
        ("Învăț română",                      "אני לומד רומנית"),
        ("Româna este grea",                  "רומנית קשה"),
        ("Româna este ușoară",                "רומנית קלה"),
        # זמן
        ("Cât este ceasul?",                  "מה השעה?"),
        ("Este ora trei",                     "השעה שלוש"),
        ("Este ora opt dimineața",            "השעה שמונה בבוקר"),
        ("Ce zi este azi?",                   "איזה יום היום?"),
        ("Azi este luni",                     "היום יום שני"),
        ("Azi este vineri",                   "היום יום שישי"),
        ("Care este data de azi?",            "מה התאריך היום?"),
        ("Azi este întâi ianuarie",           "היום הראשון לינואר"),
        ("Mâine este examenul",               "מחר הוא הבחינה"),
        ("Ieri am fost la piață",             "אתמול הלכתי לשוק"),
        # מזג אוויר
        ("Cum este vremea?",                  "מה מזג האוויר?"),
        ("Este cald azi",                     "חם היום"),
        ("Este frig",                         "קר"),
        ("Plouă",                             "יורד גשם"),
        ("Este soare",                        "יש שמש"),
        ("Bate vântul",                       "יש רוח"),
        ("Vremea este frumoasă",              "מזג האוויר נחמד"),
        ("Vremea este urâtă",                 "מזג האוויר רע"),
        ("Este înnorat",                      "מעונן"),
        # מסעדה וקניות
        ("Cât costă?",                        "כמה זה עולה?"),
        ("Nota de plată, vă rog",             "את החשבון, בבקשה"),
        ("Vreau apă",                         "אני רוצה מים"),
        ("Vreau să mănânc",                   "אני רוצה לאכול"),
        ("Mi-e foame",                        "אני רעב"),
        ("Mi-e sete",                         "אני צמא"),
        ("Aveți o masă liberă?",              "יש לכם שולחן פנוי?"),
        ("O masă pentru doi",                 "שולחן לשניים"),
        ("Meniul, vă rog",                    "את התפריט, בבקשה"),
        ("Ce recomandați?",                   "מה אתה ממליץ?"),
        ("Vreau puiul",                       "אני רוצה את העוף"),
        ("Fără ceapă, vă rog",               "בלי בצל, בבקשה"),
        ("Este foarte gustos",                "זה מאוד טעים"),
        ("Mâncarea este rece",                "האוכל קר"),
        ("Unde este supermarketul?",          "איפה הסופרמרקט?"),
        ("Aveți reduceri?",                   "יש לכם הנחה?"),
        ("Este foarte scump",                 "זה מאוד יקר"),
        ("Este ieftin",                       "זה זול"),
        ("Pot plăti cu cardul?",              "אני יכול לשלם בכרטיס?"),
        ("Îl iau",                            "אני לוקח את זה"),
        # כיוונים ותחבורה
        ("Unde este toaleta?",                "איפה השירותים?"),
        ("Unde este spitalul?",               "איפה בית החולים?"),
        ("Cum ajung în centru?",              "איך מגיעים למרכז?"),
        ("Întoarceți la dreapta",             "פנה ימינה"),
        ("Întoarceți la stânga",              "פנה שמאלה"),
        ("Mergeți drept înainte",             "המשך ישר"),
        ("Este aproape",                      "זה קרוב"),
        ("Este departe",                      "זה רחוק"),
        ("Unde este stația de autobuz?",      "איפה תחנת האוטובוס?"),
        ("Vreau un bilet la București",       "אני רוצה כרטיס לבוקרשט"),
        ("La ce oră pleacă trenul?",          "באיזו שעה יוצא הרכבת?"),
        ("Mi-am pierdut bagajul",             "אבדתי את המזוודה שלי"),
        # בריאות
        ("Mă doare capul",                    "כואב לי הראש"),
        ("Mă doare stomacul",                 "כואב לי הבטן"),
        ("Sunt bolnav",                       "אני חולה"),
        ("Am nevoie de un doctor",            "אני צריך רופא"),
        ("Am febră",                          "יש לי חום"),
        ("Sunt alergic la penicilină",        "אני אלרגי לפניצילין"),
        ("Unde este farmacia?",               "איפה בית המרקחת?"),
        ("Am nevoie de aceste pastile",       "אני צריך את הכדורים האלה"),
        ("Chemați o ambulanță",               "תקרא לאמבולנס"),
        # רגשות
        ("Sunt fericit",                      "אני שמח"),
        ("Sunt trist",                        "אני עצוב"),
        ("Sunt obosit",                       "אני עייף"),
        ("Sunt plictisit",                    "אני משועמם"),
        ("Sunt nervos",                       "אני עצבני"),
        ("Sunt entuziasmat",                  "אני נרגש"),
        ("Îmi place foarte mult",             "אני מאוד אוהב את זה"),
        ("Nu îmi place",                      "אני לא אוהב את זה"),
        ("Este foarte interesant",            "זה מאוד מעניין"),
        ("Ai dreptate",                       "אתה צודק"),
        ("Nu ai dreptate",                    "אתה לא צודק"),
        ("Sunt de acord",                     "אני מסכים"),
        ("Nu sunt de acord",                  "אני לא מסכים"),
        ("Mi se pare bine",                   "זה נראה לי בסדר"),
        ("Este o idee bună",                  "זו רעיון טוב"),
        # בית ומשפחה
        ("Locuiesc într-un apartament",       "אני גר בדירה"),
        ("Casa mea este mare",                "הבית שלי גדול"),
        ("Am două camere",                    "יש לי שני חדרים"),
        ("Câte persoane locuiesc aici?",      "כמה אנשים גרים כאן?"),
        ("Mama mea este profesoară",          "אמא שלי היא מורה"),
        ("Tatăl meu muncește mult",           "אבא שלי עובד הרבה"),
        ("Sora mea este mai mare decât mine", "האחות שלי גדולה ממני"),
        ("Am un câine",                       "יש לי כלב"),
        ("Pisica este foarte drăguță",        "החתול מאוד חמוד"),
        # לימודים ועבודה
        ("Studiez la universitate",           "אני לומד באוניברסיטה"),
        ("Am cursuri dimineața",              "יש לי שיעורים בבוקר"),
        ("Cartea este interesantă",           "הספר מעניין"),
        ("Trebuie să studiez mai mult",       "אני צריך ללמוד יותר"),
        ("Examenul a fost greu",              "הבחינה הייתה קשה"),
        ("Am luat o notă bună",               "קיבלתי ציון טוב"),
        ("Lucrez la o companie",              "אני עובד בחברה"),
        ("Am o ședință importantă",           "יש לי פגישה חשובה"),
        ("Șeful este foarte strict",          "הבוס מאוד קפדן"),
        ("Câștig un salariu bun",             "אני מרוויח משכורת טובה"),
        # פנאי
        ("Ce faci în timpul liber?",          "מה אתה עושה בזמן הפנוי?"),
        ("Îmi place să citesc",               "אני אוהב לקרוא"),
        ("Îmi place să ascult muzică",        "אני אוהב להאזין למוזיקה"),
        ("Mergem la cinema în seara asta",    "בואו נלך לקולנוע הלילה"),
        ("Filmul a fost foarte bun",          "הסרט היה מאוד טוב"),
        ("La ce oră începe?",                 "באיזו שעה זה מתחיל?"),
        ("Mergem la plajă",                   "בואו נלך לחוף הים"),
        ("Marea este foarte rece",            "הים מאוד קר"),
        ("Vrei să jucăm fotbal?",             "אתה רוצה לשחק כדורגל?"),
        ("Fac sport în fiecare zi",           "אני עושה ספורט כל יום"),
        ("Îmi place să dansez",               "אני מאוד אוהב לרקוד"),
        ("Vrei să ieșim în seara asta?",      "אתה רוצה לצאת הלילה?"),
        # טכנולוגיה
        ("Ai telefon mobil?",                 "יש לך טלפון נייד?"),
        ("Mi s-a stricat telefonul",          "הטלפון שלי התקלקל"),
        ("Pot folosi încărcătorul tău?",      "אני יכול להשתמש בטוען שלך?"),
        ("Care este parola wifi?",            "מה הסיסמה של הוויפי?"),
        ("Trimite-mi un mesaj",               "שלח לי הודעה"),
        ("Ai WhatsApp?",                      "יש לך ווטסאפ?"),
        ("Calculatorul nu funcționează",      "המחשב לא עובד"),
        ("Trebuie să printez asta",           "אני צריך להדפיס את זה"),
        # כלליות
        ("Ce mai e nou?",                     "מה נשמע?"),
        ("Ce se întâmplă?",                   "מה קורה?"),
        ("De ce?",                            "למה?"),
        ("Când?",                             "מתי?"),
        ("Cine este?",                        "מי זה?"),
        ("Ce vrei?",                          "מה אתה רוצה?"),
        ("Unde te duci?",                     "לאן אתה הולך?"),
        ("Ce mănânci?",                       "מה אתה אוכל?"),
        ("Ce crezi?",                         "מה אתה חושב?"),
        ("Cum a fost ziua ta?",               "איך היה היום שלך?"),
        ("Am nevoie de ajutor",               "אני צריך עזרה"),
        ("Chemați poliția",                   "תקרא למשטרה"),
        ("Atenție!",                          "זהירות!"),
        ("Așteptați un moment!",              "רגע אחד!"),
        ("Nicio problemă",                    "אין בעיה"),
        ("Desigur",                           "כמובן"),
        ("Uneori",                            "לפעמים"),
        ("Întotdeauna",                       "תמיד"),
        ("Niciodată",                         "אף פעם"),
        ("Vin imediat",                       "אני כבר בא"),
        ("Chiar acum",                        "עכשיו ממש"),
        ("Mai târziu",                        "מאוחר יותר"),
        ("Te iubesc",                         "אני אוהב אותך"),
        ("Totul este bine",                   "הכל בסדר"),
        ("Mă înțeleg bine cu toată lumea",   "אני מסתדר טוב עם כולם"),
        ("Am mulți prieteni",                 "יש לי הרבה חברים"),
        ("Muzica mă relaxează",               "המוזיקה מרגיעה אותי"),
    ],

    "arabic": [
        # ברכות ונימוסים
        ("صباح الخير",                        "בוקר טוב"),
        ("مساء الخير",                        "ערב טוב"),
        ("تصبح على خير",                      "לילה טוב"),
        ("مرحبا",                             "שלום"),
        ("أهلاً",                             "ברוך הבא"),
        ("مع السلامة",                        "להתראות"),
        ("إلى اللقاء",                        "להתראות"),
        ("نراك قريباً",                       "נתראה בקרוב"),
        ("فرصة سعيدة",                        "נעים להכיר"),
        ("من فضلك",                           "בבקשה"),
        ("شكراً",                             "תודה"),
        ("شكراً جزيلاً",                      "תודה רבה"),
        ("عفواً",                             "על לא דבר"),
        ("آسف",                               "אני מצטער"),
        ("المعذرة",                           "סליחה"),
        ("بصحتك",                             "לבריאות"),
        ("عيد ميلاد سعيد",                   "יום הולדת שמח"),
        ("كل عام وأنتم بخير",                "שנה טובה"),
        # היכרות
        ("كيف حالك؟",                        "מה שלומך?"),
        ("أنا بخير، شكراً",                  "אני בסדר, תודה"),
        ("أنا بخير جداً",                    "אני מאוד בסדר"),
        ("لا بأس",                            "כך כך"),
        ("اسمي محمد",                         "שמי מוחמד"),
        ("ما اسمك؟",                          "מה שמך?"),
        ("كم عمرك؟",                          "בן כמה אתה?"),
        ("عمري عشرون سنة",                   "אני בן עשרים"),
        ("من أين أنت؟",                       "מאיפה אתה?"),
        ("أنا من إسرائيل",                   "אני מישראל"),
        ("أين تسكن؟",                         "איפה אתה גר?"),
        ("أسكن في تل أبيب",                  "אני גר בתל אביב"),
        ("ما عملك؟",                          "במה אתה עובד?"),
        ("أنا طالب",                          "אני סטודנט"),
        ("أنا طبيب",                          "אני רופא"),
        ("أنا مدرس",                          "אני מורה"),
        ("عندي عائلة كبيرة",                 "יש לי משפחה גדולה"),
        ("عندي أخوان",                        "יש לי שני אחים"),
        ("أنا ولد وحيد",                     "אני בן יחיד"),
        # שפה
        ("هل تتكلم العربية؟",                "האם אתה מדבר ערבית?"),
        ("نعم، قليلاً",                       "כן, קצת"),
        ("لا أتكلم العربية",                  "אני לא מדבר ערבית"),
        ("لا أفهم",                           "אני לא מבין"),
        ("هل يمكنك أن تعيد؟",               "אתה יכול לחזור?"),
        ("تكلم ببطء أكثر",                   "דבר לאט יותר"),
        ("لا أعرف",                           "אני לא יודע"),
        ("كيف تقول هذا بالعربية؟",           "איך אומרים זאת בערבית?"),
        ("ماذا يعني هذا؟",                   "מה זה אומר?"),
        ("أنا أتعلم العربية",                "אני לומד ערבית"),
        ("العربية صعبة",                      "ערבית קשה"),
        ("العربية سهلة",                      "ערבית קלה"),
        # זמן
        ("كم الساعة؟",                        "מה השעה?"),
        ("الساعة الثالثة",                   "השעה שלוש"),
        ("الساعة الثامنة صباحاً",            "השעה שמונה בבוקר"),
        ("ما هو اليوم اليوم؟",               "איזה יום היום?"),
        ("اليوم الاثنين",                    "היום יום שני"),
        ("اليوم الجمعة",                     "היום יום שישי"),
        ("ما هو تاريخ اليوم؟",               "מה התאריך היום?"),
        ("اليوم أول يناير",                  "היום הראשון לינואר"),
        ("الامتحان غداً",                    "הבחינה היא מחר"),
        ("ذهبت إلى السوق أمس",               "הלכתי לשוק אתמול"),
        # מזג אוויר
        ("كيف الطقس؟",                        "מה מזג האוויר?"),
        ("الجو حار اليوم",                   "חם היום"),
        ("الجو بارد",                         "קר"),
        ("تمطر",                              "יורד גשם"),
        ("الشمس مشرقة",                       "יש שמש"),
        ("الريح تهب",                         "יש רוח"),
        ("الطقس جميل",                        "מזג האוויר נחמד"),
        ("الطقس سيئ",                         "מזג האוויר רע"),
        ("الجو غائم",                         "מעונן"),
        # מסעדה וקניות
        ("كم يكلف هذا؟",                     "כמה זה עולה?"),
        ("الحساب من فضلك",                   "את החשבון, בבקשה"),
        ("أريد ماء",                          "אני רוצה מים"),
        ("أريد أن آكل",                       "אני רוצה לאכול"),
        ("أنا جائع",                          "אני רעב"),
        ("أنا عطشان",                         "אני צמא"),
        ("هل عندكم طاولة حرة؟",              "יש לכם שולחן פנוי?"),
        ("طاولة لشخصين",                      "שולחן לשניים"),
        ("القائمة من فضلك",                   "את התפריט, בבקשה"),
        ("ماذا تنصح؟",                        "מה אתה ממליץ?"),
        ("أريد الدجاج",                       "אני רוצה את העוף"),
        ("بدون بصل من فضلك",                 "בלי בצל, בבקשה"),
        ("هذا لذيذ جداً",                    "זה מאוד טעים"),
        ("الطعام بارد",                       "האוכל קר"),
        ("أين السوبرماركت؟",                  "איפה הסופרמרקט?"),
        ("هل عندكم خصم؟",                    "יש לכם הנחה?"),
        ("هذا غالي جداً",                    "זה מאוד יקר"),
        ("هذا رخيص",                          "זה זול"),
        ("هل أستطيع الدفع ببطاقة؟",         "אני יכול לשלם בכרטיס?"),
        ("سآخذه",                             "אני לוקח את זה"),
        # כיוונים ותחבורה
        ("أين الحمام؟",                       "איפה השירותים?"),
        ("أين المستشفى؟",                    "איפה בית החולים?"),
        ("كيف أصل إلى المركز؟",              "איך מגיעים למרכז?"),
        ("اتجه يميناً",                       "פנה ימינה"),
        ("اتجه يساراً",                       "פנה שמאלה"),
        ("امش مباشرة",                        "המשך ישר"),
        ("هذا قريب",                          "זה קרוב"),
        ("هذا بعيد",                          "זה רחוק"),
        ("أين موقف الحافلة؟",                "איפה תחנת האוטובוס?"),
        ("أريد تذكرة إلى القدس",             "אני רוצה כרטיס לירושלים"),
        ("متى يغادر القطار؟",                "באיזו שעה יוצא הרכבת?"),
        ("فقدت حقيبتي",                       "אבדתי את המזוודה שלי"),
        # בריאות
        ("رأسي يؤلمني",                       "כואב לי הראש"),
        ("بطني تؤلمني",                       "כואב לי הבטן"),
        ("أنا مريض",                          "אני חולה"),
        ("أحتاج طبيباً",                     "אני צריך רופא"),
        ("عندي حمى",                          "יש לי חום"),
        ("أنا حساس للبنسلين",                "אני אלרגי לפניצילין"),
        ("أين الصيدلية؟",                    "איפה בית המרקחת?"),
        ("أحتاج هذه الحبوب",                 "אני צריך את הכדורים האלה"),
        ("اتصل بالإسعاف",                    "תקרא לאמבולנס"),
        # רגשות
        ("أنا سعيد",                          "אני שמח"),
        ("أنا حزين",                          "אני עצוב"),
        ("أنا تعبان",                         "אני עייף"),
        ("أنا ممل",                           "אני משועמם"),
        ("أنا متوتر",                         "אני עצבני"),
        ("أنا متحمس",                         "אני נרגש"),
        ("يعجبني كثيراً",                    "אני מאוד אוהב את זה"),
        ("لا يعجبني",                         "אני לא אוהב את זה"),
        ("هذا مثير للاهتمام جداً",           "זה מאוד מעניין"),
        ("أنت محق",                           "אתה צודק"),
        ("أنت لست محقاً",                    "אתה לא צודק"),
        ("أنا موافق",                         "אני מסכים"),
        ("أنا غير موافق",                    "אני לא מסכים"),
        ("يبدو لي جيداً",                    "זה נראה לי בסדר"),
        ("هذه فكرة جيدة",                    "זו רעיון טוב"),
        # בית ומשפחה
        ("أسكن في شقة",                      "אני גר בדירה"),
        ("بيتي كبير",                         "הבית שלי גדול"),
        ("عندي غرفتان",                       "יש לי שני חדרים"),
        ("كم شخصاً يسكن هنا؟",               "כמה אנשים גרים כאן?"),
        ("أمي مدرسة",                         "אמא שלי היא מורה"),
        ("أبي يشتغل كثيراً",                 "אבא שלי עובד הרבה"),
        ("أختي أكبر مني",                    "האחות שלי גדולה ממני"),
        ("عندي كلب",                          "יש לי כלב"),
        ("القطة جميلة جداً",                 "החתולה מאוד יפה"),
        # לימודים ועבודה
        ("أنا أدرس في الجامعة",              "אני לומד באוניברסיטה"),
        ("عندي محاضرات في الصباح",           "יש לי שיעורים בבוקר"),
        ("الكتاب ممتع",                       "הספר מעניין"),
        ("يجب أن أدرس أكثر",                 "אני צריך ללמוד יותר"),
        ("الامتحان كان صعباً",               "הבחינה הייתה קשה"),
        ("حصلت على درجة جيدة",               "קיבלתי ציון טוב"),
        ("أعمل في شركة",                     "אני עובד בחברה"),
        ("عندي اجتماع مهم",                  "יש לי פגישה חשובה"),
        ("المدير صارم جداً",                 "הבוס מאוד קפדן"),
        ("راتبي جيد",                         "אני מרוויח משכורת טובה"),
        # פנאי
        ("ماذا تفعل في وقت فراغك؟",          "מה אתה עושה בזמן הפנוי?"),
        ("أحب القراءة",                       "אני אוהב לקרוא"),
        ("أحب سماع الموسيقى",                "אני אוהב להאזין למוזיקה"),
        ("نذهب إلى السينما الليلة",          "בואו נלך לקולנוע הלילה"),
        ("الفيلم كان جيداً جداً",            "הסרט היה מאוד טוב"),
        ("في أي ساعة يبدأ؟",                 "באיזו שעה זה מתחיל?"),
        ("نذهب إلى الشاطئ",                  "בואו נלך לחוף הים"),
        ("البحر بارد جداً",                  "הים מאוד קר"),
        ("هل تريد أن تلعب كرة القدم؟",      "אתה רוצה לשחק כדורגל?"),
        ("أمارس الرياضة كل يوم",             "אני עושה ספורט כל יום"),
        ("أحب الرقص",                         "אני מאוד אוהב לרקוד"),
        ("هل تريد الخروج الليلة؟",           "אתה רוצה לצאת הלילה?"),
        # טכנולוגיה
        ("هل عندك هاتف جوال؟",               "יש לך טלפון נייד?"),
        ("هاتفي تعطل",                        "הטלפון שלי התקלקל"),
        ("هل أستطيع استخدام شاحنتك؟",       "אני יכול להשתמש בטוען שלך?"),
        ("ما كلمة مرور الواي فاي؟",          "מה הסיסמה של הוויפי?"),
        ("أرسل لي رسالة",                    "שלח לי הודעה"),
        ("هل عندك واتساب؟",                  "יש לך ווטסאפ?"),
        ("الكمبيوتر لا يعمل",                "המחשב לא עובד"),
        ("أحتاج إلى طباعة هذا",              "אני צריך להדפיס את זה"),
        # כלליות
        ("ما الأخبار؟",                       "מה נשמע?"),
        ("ماذا يجري؟",                        "מה קורה?"),
        ("لماذا؟",                            "למה?"),
        ("متى؟",                              "מתי?"),
        ("من هذا؟",                           "מי זה?"),
        ("ماذا تريد؟",                        "מה אתה רוצה?"),
        ("إلى أين تذهب؟",                    "לאן אתה הולך?"),
        ("ماذا تأكل؟",                        "מה אתה אוכל?"),
        ("ماذا تعتقد؟",                       "מה אתה חושב?"),
        ("كيف كان يومك؟",                    "איך היה היום שלך?"),
        ("أحتاج مساعدة",                     "אני צריך עזרה"),
        ("اتصل بالشرطة",                     "תקרא למשטרה"),
        ("انتبه!",                             "זהירות!"),
        ("انتظر لحظة!",                       "רגע אחד!"),
        ("لا مشكلة",                          "אין בעיה"),
        ("بالطبع",                            "כמובן"),
        ("أحياناً",                           "לפעמים"),
        ("دائماً",                            "תמיד"),
        ("أبداً",                             "אף פעם"),
        ("آتي الآن",                          "אני כבר בא"),
        ("الآن فوراً",                        "עכשיו ממש"),
        ("لاحقاً",                            "מאוחר יותר"),
        ("أحبك",                              "אני אוהב אותך"),
        ("كل شيء بخير",                      "הכל בסדר"),
        ("أنا أتعامل مع الجميع بشكل جيد",  "אני מסתדר טוב עם כולם"),
        ("عندي أصدقاء كثيرون",               "יש לי הרבה חברים"),
        ("الموسيقى تريحني",                   "המוזיקה מרגיעה אותי"),
    ],
}

LANG_META = {
    "spanish":  {"label": "ספרדית",  "flag": "🇪🇸", "source_label": "המשפט בספרדית",   "dir": "ltr"},
    "english":  {"label": "אנגלית",  "flag": "🇬🇧", "source_label": "המשפט באנגלית",   "dir": "ltr"},
    "romanian": {"label": "רומנית",  "flag": "🇷🇴", "source_label": "המשפט ברומנית",   "dir": "ltr"},
    "arabic":   {"label": "ערבית",   "flag": "🇸🇦", "source_label": "המשפט בערבית",    "dir": "rtl"},
}


def strip_punct(text):
    return re.sub(r'[?!.,،؟¡¿]', '', text).strip()

def normalize(text):
    return strip_punct(text).lower()

def find_issues(user_input, correct):
    u = user_input.strip().split()
    c = correct.strip().split()
    issues = []
    for i in range(max(len(u), len(c))):
        if i >= len(u):
            issues.append(f"חסרה המילה: «{c[i]}»")
        elif i >= len(c):
            issues.append(f"מילה מיותרת: «{u[i]}»")
        elif normalize(u[i]) != normalize(c[i]):
            issues.append(f"«{u[i]}» => צריך להיות «{c[i]}»")
    return issues


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    session.pop("lang", None)
    return render_template_string(SELECT_HTML)

@app.route("/select/<lang>")
def select_lang(lang):
    if lang not in LANG_META:
        return redirect(url_for("index"))
    session.clear()
    session["lang"] = lang
    session["used"] = []
    session["stats"] = {"first_try": 0, "corrected": 0, "words": 0}
    session["attempts"] = 0
    session["current"] = None
    return redirect(url_for("train"))

@app.route("/train")
def train():
    lang = session.get("lang")
    if not lang or lang not in LANG_META:
        return redirect(url_for("index"))
    meta = LANG_META[lang]
    return render_template_string(TRAIN_HTML, lang=lang, meta=meta)

@app.route("/api/sentence")
def get_sentence():
    lang = session.get("lang", "spanish")
    sentences = SENTENCES[lang]
    used = session.get("used", [])
    remaining = [i for i in range(len(sentences)) if i not in used]
    if not remaining:
        used = []
        remaining = list(range(len(sentences)))
    idx = random.choice(remaining)
    used.append(idx)
    session["used"] = used
    session["current"] = idx
    session["attempts"] = 0
    return jsonify({"id": idx, "source": sentences[idx][0]})

@app.route("/api/check", methods=["POST"])
def check():
    lang = session.get("lang", "spanish")
    sentences = SENTENCES[lang]
    data = request.get_json()
    idx = session.get("current")
    if idx is None:
        return jsonify({"error": "no sentence"}), 400
    user_answer = data.get("answer", "").strip()
    _, hebrew = sentences[idx]
    session["attempts"] = session.get("attempts", 0) + 1
    attempts = session["attempts"]

    if normalize(user_answer) == normalize(hebrew):
        stats = session.get("stats", {"first_try": 0, "corrected": 0, "words": 0})
        word_count = len(hebrew.split())
        stats["words"] += word_count
        if attempts == 1:
            stats["first_try"] += 1
            first_try = True
        else:
            stats["corrected"] += 1
            first_try = False
        session["stats"] = stats
        session["current"] = None
        return jsonify({"correct": True, "first_try": first_try, "attempts": attempts, "hebrew": hebrew})
    else:
        issues = find_issues(user_answer, hebrew)
        return jsonify({"correct": False, "issues": issues, "attempts": attempts})

@app.route("/api/stats")
def get_stats():
    return jsonify(session.get("stats", {"first_try": 0, "corrected": 0, "words": 0}))

@app.route("/api/reset")
def reset():
    lang = session.get("lang")
    session.clear()
    if lang:
        session["lang"] = lang
    return jsonify({"ok": True})


# ── Language selection page ────────────────────────────────────────────────────

SELECT_HTML = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>בחר שפה ללימוד</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Segoe UI',Arial,sans-serif;
  background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);
  min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px;
}
.card{
  background:rgba(255,255,255,0.06);
  backdrop-filter:blur(12px);
  border:1px solid rgba(255,255,255,0.12);
  border-radius:24px;padding:48px 40px;
  max-width:540px;width:100%;color:#e0e0e0;
  text-align:center;
}
h1{font-size:1.8rem;color:#fff;margin-bottom:8px}
.subtitle{font-size:.9rem;color:#888;margin-bottom:40px}
.langs{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.lang-btn{
  display:flex;flex-direction:column;align-items:center;gap:12px;
  padding:28px 20px;border-radius:18px;border:2px solid rgba(255,255,255,0.1);
  background:rgba(255,255,255,0.05);cursor:pointer;text-decoration:none;
  color:#e0e0e0;transition:all .22s;
}
.lang-btn:hover{
  border-color:rgba(233,69,96,0.6);
  background:rgba(233,69,96,0.1);
  transform:translateY(-3px);
  box-shadow:0 8px 32px rgba(233,69,96,0.15);
}
.flag{font-size:3rem;line-height:1}
.lang-name{font-size:1.25rem;font-weight:700;color:#fff}
.lang-sub{font-size:.78rem;color:#888}
</style>
</head>
<body>
<div class="card">
  <h1>בחר שפה ללימוד</h1>
  <p class="subtitle">תרגם משפטים מהשפה הנבחרת לעברית</p>
  <div class="langs">
    <a class="lang-btn" href="/select/spanish">
      <span class="flag">🇪🇸</span>
      <span class="lang-name">ספרדית</span>
      <span class="lang-sub">Español</span>
    </a>
    <a class="lang-btn" href="/select/english">
      <span class="flag">🇬🇧</span>
      <span class="lang-name">אנגלית</span>
      <span class="lang-sub">English</span>
    </a>
    <a class="lang-btn" href="/select/romanian">
      <span class="flag">🇷🇴</span>
      <span class="lang-name">רומנית</span>
      <span class="lang-sub">Română</span>
    </a>
    <a class="lang-btn" href="/select/arabic">
      <span class="flag">🇸🇦</span>
      <span class="lang-name">ערבית</span>
      <span class="lang-sub">العربية</span>
    </a>
  </div>
</div>
</body>
</html>"""


# ── Training page ──────────────────────────────────────────────────────────────

TRAIN_HTML = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>אימון {{ meta.label }}</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Segoe UI',Arial,sans-serif;
  background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);
  min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px;
}
.card{
  background:rgba(255,255,255,0.06);
  backdrop-filter:blur(12px);
  border:1px solid rgba(255,255,255,0.12);
  border-radius:24px;padding:40px 36px;
  max-width:580px;width:100%;color:#e0e0e0;
}
.top-row{display:flex;align-items:center;justify-content:space-between;margin-bottom:6px}
h1{font-size:1.5rem;color:#e94560}
.change-lang{
  font-size:.78rem;color:#888;text-decoration:none;
  border:1px solid rgba(255,255,255,0.12);border-radius:8px;
  padding:5px 12px;transition:all .2s;
}
.change-lang:hover{color:#fff;border-color:rgba(255,255,255,0.35)}
.subtitle{text-align:center;font-size:.82rem;color:#777;margin-bottom:28px}

.stats-bar{display:flex;gap:10px;justify-content:center;margin-bottom:24px;flex-wrap:wrap}
.stat{
  background:rgba(255,255,255,0.07);border-radius:10px;
  padding:8px 16px;text-align:center;font-size:.8rem;color:#aaa;
}
.stat span{display:block;font-size:1.2rem;font-weight:700;color:#fff;margin-bottom:2px}
.stat.green span{color:#60d080}
.stat.yellow span{color:#f0c040}
.stat.blue span{color:#60b0ff}

.label{font-size:.78rem;color:#888;margin-bottom:6px;text-transform:uppercase;letter-spacing:.05em}
.source{
  background:rgba(233,69,96,0.12);border:1px solid rgba(233,69,96,0.3);
  border-radius:14px;padding:22px;text-align:center;
  font-size:1.7rem;font-weight:700;color:#fff;margin-bottom:24px;
  letter-spacing:.02em;min-height:72px;display:flex;align-items:center;justify-content:center;
  direction:{{ meta.dir }};
}
.input-row{display:flex;gap:10px;margin-bottom:14px}
input[type=text]{
  flex:1;padding:13px 16px;border-radius:11px;
  border:1px solid rgba(255,255,255,0.15);background:rgba(255,255,255,0.07);
  color:#fff;font-size:1rem;direction:rtl;outline:none;
  transition:border-color .2s;
}
input[type=text]:focus{border-color:#e94560}
input::placeholder{color:#444}
button{
  padding:13px 22px;border-radius:11px;border:none;
  background:#e94560;color:#fff;font-size:.95rem;font-weight:700;
  cursor:pointer;transition:background .2s,transform .1s;white-space:nowrap;
}
button:hover{background:#c73652}
button:active{transform:scale(.97)}
button:disabled{background:#555;cursor:default}

.feedback{
  border-radius:12px;padding:16px;font-size:.92rem;
  line-height:1.8;margin-bottom:12px;display:none;
}
.feedback.wrong{
  display:block;background:rgba(255,80,80,.1);
  border:1px solid rgba(255,80,80,.3);color:#ff9090;
}
.feedback.correct{
  display:block;background:rgba(50,200,100,.1);
  border:1px solid rgba(50,200,100,.3);color:#70e090;
  text-align:center;font-size:1.05rem;
}
.issue{display:block}

.bottom-row{display:flex;gap:10px;justify-content:center;margin-top:4px}
.btn-next{background:#1a3a6a;border:1px solid rgba(255,255,255,.15);display:none}
.btn-next:hover{background:#254d90}
.btn-summary{background:#3a1a5a;border:1px solid rgba(255,255,255,.15);display:none}
.btn-summary:hover{background:#502080}

.overlay{
  display:none;position:fixed;inset:0;
  background:rgba(0,0,0,.7);align-items:center;justify-content:center;z-index:10;
}
.overlay.show{display:flex}
.summary-box{
  background:#1a1a2e;border:1px solid rgba(255,255,255,.15);
  border-radius:20px;padding:36px;max-width:420px;width:90%;text-align:center;color:#e0e0e0;
}
.summary-box h2{color:#e94560;margin-bottom:20px;font-size:1.3rem}
.summary-row{
  display:flex;justify-content:space-between;
  padding:10px 0;border-bottom:1px solid rgba(255,255,255,.07);font-size:.95rem;
}
.summary-row:last-of-type{border:none}
.summary-row .val{font-weight:700;color:#fff}
.btn-restart{margin-top:22px;background:#e94560;width:100%;padding:14px;font-size:1rem}
.btn-change{margin-top:10px;background:#2a1a4a;width:100%;padding:12px;font-size:.9rem;border:1px solid rgba(255,255,255,.15)}
.btn-change:hover{background:#3a2a6a}
</style>
</head>
<body>
<div class="card">
  <div class="top-row">
    <h1>{{ meta.flag }} אימון {{ meta.label }}</h1>
    <a class="change-lang" href="/">החלף שפה</a>
  </div>
  <p class="subtitle">תרגם את המשפט מ{{ meta.label }} לעברית</p>

  <div class="stats-bar">
    <div class="stat green"><span id="s-first">0</span>צדקת מהניסיון הראשון</div>
    <div class="stat yellow"><span id="s-corr">0</span>תיקנת</div>
    <div class="stat blue"><span id="s-words">0</span>מילים</div>
  </div>

  <div class="label">{{ meta.source_label }}</div>
  <div class="source" id="source">טוען...</div>

  <div class="label">התרגום שלך לעברית</div>
  <div class="input-row">
    <input type="text" id="answer" placeholder="כתוב כאן..." autocomplete="off"/>
    <button id="btn-check" onclick="checkAnswer()">בדוק</button>
  </div>

  <div class="feedback" id="feedback"></div>

  <div class="bottom-row">
    <button class="btn-next" id="btn-next" onclick="nextSentence()">משפט הבא &larr;</button>
    <button class="btn-summary" id="btn-summary" onclick="showSummary()">סיכום</button>
  </div>
</div>

<div class="overlay" id="overlay">
  <div class="summary-box">
    <h2>סיכום האימון</h2>
    <div class="summary-row"><span>משפטים שענית עליהם</span><span class="val" id="sum-total">0</span></div>
    <div class="summary-row"><span>צדקת מהניסיון הראשון</span><span class="val" id="sum-first">0</span></div>
    <div class="summary-row"><span>טעית ותיקנת</span><span class="val" id="sum-corr">0</span></div>
    <div class="summary-row"><span>סה"כ מילים</span><span class="val" id="sum-words">0</span></div>
    <button class="btn-restart" onclick="restart()">התחל מחדש</button>
    <button class="btn-change" onclick="window.location='/'">החלף שפה</button>
  </div>
</div>

<script>
let solved = false;

async function loadSentence() {
  solved = false;
  document.getElementById('answer').value = '';
  document.getElementById('answer').disabled = false;
  document.getElementById('btn-check').disabled = false;
  document.getElementById('feedback').className = 'feedback';
  document.getElementById('feedback').innerHTML = '';
  document.getElementById('btn-next').style.display = 'none';
  document.getElementById('btn-summary').style.display = 'none';
  document.getElementById('source').textContent = '...';

  const res = await fetch('/api/sentence');
  const data = await res.json();
  document.getElementById('source').textContent = data.source;
  document.getElementById('answer').focus();
}

async function checkAnswer() {
  if (solved) return;
  const answer = document.getElementById('answer').value.trim();
  if (!answer) return;

  const res = await fetch('/api/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({answer})
  });
  const data = await res.json();
  const fb = document.getElementById('feedback');

  if (data.correct) {
    solved = true;
    document.getElementById('answer').disabled = true;
    document.getElementById('btn-check').disabled = true;
    fb.className = 'feedback correct';
    const msg = data.first_try ? 'מעולה! צדקת מהניסיון הראשון!' : `צדקת אחרי ${data.attempts} ניסיונות.`;
    fb.innerHTML = `<strong>${msg}</strong><br>התרגום: ${data.hebrew}`;
    document.getElementById('btn-next').style.display = 'inline-block';
    document.getElementById('btn-summary').style.display = 'inline-block';
    await updateStats();
  } else {
    fb.className = 'feedback wrong';
    fb.innerHTML = '<strong>לא מדויק. מה שצריך לתקן:</strong><br>' +
      data.issues.map(i => `<span class="issue">• ${i}</span>`).join('');
    document.getElementById('answer').focus();
    document.getElementById('answer').select();
  }
}

async function updateStats() {
  const res = await fetch('/api/stats');
  const s = await res.json();
  document.getElementById('s-first').textContent = s.first_try;
  document.getElementById('s-corr').textContent = s.corrected;
  document.getElementById('s-words').textContent = s.words;
}

function nextSentence() { loadSentence(); }

async function showSummary() {
  const res = await fetch('/api/stats');
  const s = await res.json();
  document.getElementById('sum-total').textContent = s.first_try + s.corrected;
  document.getElementById('sum-first').textContent = s.first_try;
  document.getElementById('sum-corr').textContent = s.corrected;
  document.getElementById('sum-words').textContent = s.words;
  document.getElementById('overlay').classList.add('show');
}

async function restart() {
  await fetch('/api/reset');
  document.getElementById('overlay').classList.remove('show');
  document.getElementById('s-first').textContent = '0';
  document.getElementById('s-corr').textContent = '0';
  document.getElementById('s-words').textContent = '0';
  loadSentence();
}

document.getElementById('answer').addEventListener('keydown', e => {
  if (e.key === 'Enter') checkAnswer();
});

loadSentence();
</script>
</body>
</html>"""

if __name__ == "__main__":
    print("האפליקציה רצה על: http://localhost:5000")
    app.run(debug=False, port=5000)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import random
from flask import Flask, jsonify, request, session, render_template_string

app = Flask(__name__)
app.secret_key = "spanish-trainer-secret-2024"

SENTENCES = [
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
    ("¿Dónde vives?",                    "איפה אתה גר?"),
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
    ("El agua está fría",                 "המים קרים"),
    ("Te quiero",                         "אני אוהב אותך"),
    ("Sé que sí",                        "אני יודע שכן"),
    ("Vivo en Israel",                    "אני גר בישראל"),
    ("El cielo es azul",                  "השמיים כחולים"),
    ("La vida es bella",                  "החיים יפים"),
    ("Todo está bien",                    "הכל בסדר"),
    ("Me llevo bien con todos",           "אני מסתדר טוב עם כולם"),
    ("Tengo muchos amigos",               "יש לי הרבה חברים"),
    ("La música me relaja",               "המוזיקה מרגיעה אותי"),
]


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


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    session.setdefault("used", [])
    session.setdefault("stats", {"first_try": 0, "corrected": 0, "words": 0})
    session.setdefault("attempts", 0)
    session.setdefault("current", None)
    return render_template_string(HTML)

@app.route("/api/sentence")
def get_sentence():
    used = session.get("used", [])
    remaining = [i for i in range(len(SENTENCES)) if i not in used]
    if not remaining:
        used = []
        remaining = list(range(len(SENTENCES)))
    idx = random.choice(remaining)
    used.append(idx)
    session["used"] = used
    session["current"] = idx
    session["attempts"] = 0
    return jsonify({"id": idx, "spanish": SENTENCES[idx][0]})

@app.route("/api/check", methods=["POST"])
def check():
    data = request.get_json()
    idx = session.get("current")
    if idx is None:
        return jsonify({"error": "no sentence"}), 400
    user_answer = data.get("answer", "").strip()
    _, hebrew = SENTENCES[idx]
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
    session.clear()
    return jsonify({"ok": True})


# ── HTML ──────────────────────────────────────────────────────────────────────

HTML = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>אימון ספרדית</title>
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
h1{text-align:center;font-size:1.5rem;color:#e94560;margin-bottom:6px}
.subtitle{text-align:center;font-size:.82rem;color:#777;margin-bottom:28px}

/* stats bar */
.stats-bar{
  display:flex;gap:10px;justify-content:center;margin-bottom:24px;flex-wrap:wrap;
}
.stat{
  background:rgba(255,255,255,0.07);border-radius:10px;
  padding:8px 16px;text-align:center;font-size:.8rem;color:#aaa;
}
.stat span{display:block;font-size:1.2rem;font-weight:700;color:#fff;margin-bottom:2px}
.stat.green span{color:#60d080}
.stat.yellow span{color:#f0c040}
.stat.blue span{color:#60b0ff}

.label{font-size:.78rem;color:#888;margin-bottom:6px;text-transform:uppercase;letter-spacing:.05em}
.spanish{
  background:rgba(233,69,96,0.12);border:1px solid rgba(233,69,96,0.3);
  border-radius:14px;padding:22px;text-align:center;
  font-size:1.7rem;font-weight:700;color:#fff;margin-bottom:24px;
  letter-spacing:.02em;min-height:72px;display:flex;align-items:center;justify-content:center;
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

/* summary overlay */
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
</style>
</head>
<body>
<div class="card">
  <h1>אימון ספרדית</h1>
  <p class="subtitle">תרגם את המשפט מספרדית לעברית</p>

  <div class="stats-bar">
    <div class="stat green"><span id="s-first">0</span>צדקת מהניסיון הראשון</div>
    <div class="stat yellow"><span id="s-corr">0</span>תיקנת</div>
    <div class="stat blue"><span id="s-words">0</span>מילים</div>
  </div>

  <div class="label">המשפט בספרדית</div>
  <div class="spanish" id="spanish">טוען...</div>

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

<!-- Summary overlay -->
<div class="overlay" id="overlay">
  <div class="summary-box">
    <h2>סיכום האימון</h2>
    <div class="summary-row"><span>משפטים שענית עליהם</span><span class="val" id="sum-total">0</span></div>
    <div class="summary-row"><span>צדקת מהניסיון הראשון</span><span class="val" id="sum-first">0</span></div>
    <div class="summary-row"><span>טעית ותיקנת</span><span class="val" id="sum-corr">0</span></div>
    <div class="summary-row"><span>סה"כ מילים</span><span class="val" id="sum-words">0</span></div>
    <button class="btn-restart" onclick="restart()">התחל מחדש</button>
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
  document.getElementById('spanish').textContent = '...';

  const res = await fetch('/api/sentence');
  const data = await res.json();
  document.getElementById('spanish').textContent = data.spanish;
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

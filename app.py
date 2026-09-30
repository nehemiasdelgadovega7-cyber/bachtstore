import speech_recognition as sr
import difflib
from google import genai
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class AppIngles(BoxLayout):
    def __init__(self, api_key, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10, **kwargs)

        # Configurar cliente Gemini
        self.client = genai.Client(api_key=api_key)

        # Misiones básicas
        self.misiones = {
            1: {"frase": "Hello, how are you?", "completada": False},
            2: {"frase": "I am learning English.", "completada": False},
            3: {"frase": "Can you help me, please?", "completada": False},
        }
        self.nivel_actual = 1

        # Escenarios con medallas
        self.escenarios = {
            "🍽️ Restaurante": {
                "dialogo": [
                    "Waiter: Hello, welcome! What would you like to order?",
                    "Waiter: Anything to drink?",
                    "Waiter: Great choice! Your food will be ready soon."
                ],
                "medalla": "🥇 Chef"
            },
            "✈️ Aeropuerto": {
                "dialogo": [
                    "Agent: Can I see your passport?",
                    "Agent: Where are you traveling today?",
                    "Agent: Thank you, have a safe flight!"
                ],
                "medalla": "✈️ Traveler"
            }
        }
        self.escenario_actual = None
        self.indice = 0
        self.medallas_obtenidas = []
        self.errores = {}

        # Etiqueta principal
        self.log = Label(
            text="🎯 Bienvenido a tu app de inglés\nSelecciona una misión o escenario",
            halign="center"
        )
        self.add_widget(self.log)

        # Botones principales
        self.add_widget(Button(text="📖 Practicar misión", size_hint=(1, 0.2), on_press=self.practicar_mision))
        self.add_widget(Button(text="➡️ Avanzar misión", size_hint=(1, 0.2), on_press=self.avanzar_mision))
        self.add_widget(Button(text="🎭 Escenario Restaurante", size_hint=(1, 0.2),
                               on_press=lambda x: self.seleccionar_escenario("🍽️ Restaurante")))
        self.add_widget(Button(text="✈️ Escenario Aeropuerto", size_hint=(1, 0.2),
                               on_press=lambda x: self.seleccionar_escenario("✈️ Aeropuerto")))
        self.add_widget(Button(text="🎤 Responder escenario", size_hint=(1, 0.2), on_press=self.responder_escenario))
        self.add_widget(Button(text="➡️ Siguiente diálogo", size_hint=(1, 0.2), on_press=self.avanzar_escenario))
        self.add_widget(Button(text="🏅 Ver medallas", size_hint=(1, 0.2), on_press=self.ver_medallas))
        self.add_widget(Button(text="📊 Ver estadísticas", size_hint=(1, 0.2), on_press=self.ver_estadisticas))

    # -------------------
    # Funciones generales
    # -------------------
    def escuchar(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.log.text = "🎙️ Habla ahora..."
            audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio)
        except:
            return "⚠️ No se pudo reconocer tu voz."

    def retroalimentacion(self, frase_dicha):
        prompt = f"""
        Analiza la siguiente frase en inglés: "{frase_dicha}"
        - Indica si la gramática es correcta.
        - Señala errores de vocabulario o palabras mal usadas.
        - Da una versión corregida de la frase.
        """
        model = self.client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        return model.text

    # -------------------
    # Misiones
    # -------------------
    def practicar_mision(self, instance):
        frase = self.misiones[self.nivel_actual]["frase"]
        dicho = self.escuchar()
        similitud = difflib.SequenceMatcher(None, frase.lower(), dicho.lower()).ratio()

        if similitud > 0.8:
            self.log.text = f"✅ Correcto: {dicho}\n+50 XP"
            self.misiones[self.nivel_actual]["completada"] = True
        else:
            self.log.text = f"❌ Dijiste: {dicho}\nFrase correcta: {frase}"
            self.errores[frase] = self.errores.get(frase, 0) + 1

        self.log.text += f"\n📊 Feedback:\n{self.retroalimentacion(dicho)}"

    def avanzar_mision(self, instance):
        if self.misiones[self.nivel_actual]["completada"]:
            self.nivel_actual += 1
            if self.nivel_actual in self.misiones:
                self.log.text = f"🎯 Nueva misión: {self.misiones[self.nivel_actual]['frase']}"
            else:
                self.log.text = "🏆 ¡Has completado todas las misiones!"
        else:
            self.log.text += "\n❌ Completa la misión antes de avanzar."

    # -------------------
    # Escenarios
    # -------------------
    def seleccionar_escenario(self, nombre):
        self.escenario_actual = nombre
        self.indice = 0
        self.log.text = f"🎭 Escenario: {nombre}\n{self.escenarios[nombre]['dialogo'][self.indice]}"

    def responder_escenario(self, instance):
        if self.escenario_actual:
            respuesta = self.escuchar()
            feedback = self.retroalimentacion(respuesta)
            self.log.text = f"🗣️ Tu respuesta: {respuesta}\n📊 Feedback:\n{feedback}"
        else:
            self.log.text = "⚠️ Selecciona un escenario primero."

    def avanzar_escenario(self, instance):
        if self.escenario_actual:
            self.indice += 1
            if self.indice < len(self.escenarios[self.escenario_actual]["dialogo"]):
                self.log.text = f"🎭 Escenario: {self.escenario_actual}\n{self.escenarios[self.escenario_actual]['dialogo'][self.indice]}"
            else:
                medalla = self.escenarios[self.escenario_actual]["medalla"]
                self.medallas_obtenidas.append(medalla)
                self.log.text = f"🏆 Escenario completado: {self.escenario_actual}\nHas ganado la medalla {medalla}"
        else:
            self.log.text = "⚠️ Selecciona un escenario primero."

    # -------------------
    # Medallas y estadísticas
    # -------------------
    def ver_medallas(self, instance):
        if self.medallas_obtenidas:
            texto = "🏅 Medallas obtenidas:\n" + "\n".join(self.medallas_obtenidas)
        else:
            texto = "Aún no tienes medallas."
        self.log.text = texto

    def ver_estadisticas(self, instance):
        texto = "📊 Estadísticas:\n"
        texto += f"✅ Misiones completadas: {sum(1 for m in self.misiones.values() if m['completada'])}\n"
        texto += "❌ Errores:\n"
        for frase, veces in self.errores.items():
            texto += f"- {frase}: {veces} errores\n"
        texto += f"🏅 Medallas: {', '.join(self.medallas_obtenidas) if self.medallas_obtenidas else 'Ninguna'}"
        self.log.text = texto


class AppInglesMain(App):
    def build(self):
        return AppIngles(api_key="AQ.Ab8RN6LWR55xM-U8CnBzK3ZDQnutyOT0ao-bg1S0r1sI5xRKEw")


if __name__ == "__main__":
    AppInglesMain().run()

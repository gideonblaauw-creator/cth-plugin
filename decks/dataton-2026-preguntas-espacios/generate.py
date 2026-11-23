#!/usr/bin/env python3
"""Generate index.html for Datatón preguntas por espacio (17 pages)."""
from __future__ import annotations

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "index.html"

SPACES = [
    {
        "time": "08:30",
        "title": "Palabras de apertura",
        "participants": "Gideon Blaauw (CleantechHUB), Gloria Marlene Díaz (Centro de Emprendimiento, Externado)",
        "asks": "Gideon y Marlene -> audiencia",
        "viene": "Registro: participantes con credencial y expectativa del día.",
        "lleva": "Marco del día: territorio -> observatorio -> caso -> equipos.",
        "turns": [
            (
                "¿Por qué hoy unen la universidad y CleantechHUB en un mismo escenario?",
                "Porque la pregunta territorial ya no cabe en un solo silo: hace falta colaboración con datos verificables.",
                "¿Qué significa para ustedes «Observa. Actúa. Transforma.» en una sola frase?",
            ),
            (
                "Marlene, ¿qué le dice a los equipos que hoy trabajan el lienzo de modelo de negocio por primera vez?",
                "En Externado veníamos del «Modelo y Más»; hoy el lienzo abre una conversación nueva sobre dónde vive el dato.",
                "¿Cómo les pide que usen los datos propios sin sobreprometer lo que aún no pueden medir?",
            ),
            (
                "¿Qué prometen al auditorio respecto al Observatorio y al motor del Datalab?",
                "Un vocabulario común: el programa se nombra hoy; el laboratorio es el motor dentro de él.",
                "¿Qué dejan explícito sobre certificados y seguimiento a quienes no pasen a la final?",
            ),
            (
                "¿Qué imagen macro quieren que el público se lleve antes del panel?",
                "De paisaje y cooperación a decisiones con evidencia: el territorio primero, el caso después.",
                "¿Con qué pregunta territorial quieren que arranque el panel de las once menos veinte?",
            ),
        ],
        "puente": "Abrimos el panel: ¿quién transporta la presión y quién puede adoptar en el territorio?",
        "fuente": "Fuente: agenda v7, reunión logística 23 nov",
    },
    {
        "time": "08:40",
        "title": "Panel: innovación y emprendimiento en el territorio a través de los datos (ODS 13)",
        "participants": "Natalia Vargas (APC-Colombia), rector o representante Universidad Externado, RAP Pacífico, Óscar (Apix Pharma); moderador Gideon",
        "asks": "Gideon -> panelistas",
        "viene": "Apertura: día como hilo macro -> micro con datos.",
        "lleva": "Preguntas territoriales que el Observatorio recoge a las nueve diez.",
        "turns": [
            (
                "Natalia, desde la cooperación: ¿qué presión internacional llega al territorio que no puede ignorarse?",
                "La cooperación transporta exigencias de trazabilidad y climática; no es el paisaje en sí, pero lo activa.",
                "¿Qué rol ve para la academia cuando esa presión choca con capacidad local?",
            ),
            (
                "Rector, ¿cómo articula la universidad gobierno, empresa y sociedad sin volverse un «sexto actor»?",
                "La universidad formula la pregunta y sostiene ética del dato; no es un radio más de la hélice.",
                "¿Qué decisión territorial le gustaría ver respaldada por datos abiertos este año?",
            ),
            (
                "RAP Pacífico: ¿qué dolor del Pacífico merece un tablero, no un discurso?",
                "Presiones de biodiversidad y economías locales que necesitan evidencia antes de invertir.",
                "¿Con qué actor del régimen necesita sentarse primero para que el dato sea cit-able?",
            ),
            (
                "Óscar, desde empresa: ¿qué indicador de sostenibilidad le falta ver antes de adoptar innovación?",
                "Aire limpio y ODS 13 en instalaciones sensibles; necesitamos ver lo invisible antes de comprar.",
                "Si Apix no está hoy: ¿qué pregunta deja el cuarto vértice de la hélice sobre el papel?",
            ),
            (
                "Cierre al panel: ¿en una frase, qué pregunta le entregan ustedes al lanzamiento del Observatorio?",
                "¿Cómo convertimos colaboración en capacidad verificable con datos que aguantan conclusión?",
                "¿Quién en esta sala se ofrece como adoptante si la evidencia llega en nivel Oro?",
            ),
        ],
        "puente": "Pasamos a nombrar el programa y su motor: Observatorio de la Tierra y Datalab.",
        "fuente": "Fuente: agenda v7, nota agenda 23 nov, propuesta EO (frases cortas)",
    },
    {
        "time": "09:10",
        "title": "Lanzamiento del Observatorio de la Tierra y presentación del Datalab",
        "participants": "Gideon Blaauw, Diego Alejandro Díaz Malagón (Desarrollo e Innovación, Externado)",
        "asks": "Gideon -> audiencia; Alejandro Díaz -> academia",
        "viene": "Panel: dolores y preguntas territoriales (ODS 13).",
        "lleva": "Vocabulario nicho / régimen / paisaje y entornos del Datalab.",
        "turns": [
            (
                "¿Por qué «Observatorio de la Tierra» y no otro nombre para este programa?",
                "Es el lugar donde casa académica y custodia trabajan juntas con la hélice.",
                "¿Cómo explican Carapulica sin convertirlo en un almacén de datos?",
            ),
            (
                "¿Qué es el Datalab dentro de ese relato?",
                "El motor dentro del observatorio; el dato queda debajo, como infraestructura.",
                "¿Cuáles son los cuatro entornos que hoy pueden nombrar sin prometer pilotos cerrados?",
            ),
            (
                "Alejandro, ¿qué aporta Externado que no sea «más otra aceleradora»?",
                "Estudiantes, ética y revisión de si el dato aguanta conclusión.",
                "¿Cómo conectan las cinco palancas del programa con lo que veremos en el sandbox?",
            ),
            (
                "¿En qué fase estamos hoy con este datatón?",
                "Entorno datathon del motor: semanas de reglas de evento, puente hacia un piloto por lente.",
                "¿Qué NO es el Observatorio, para alinear expectativas?",
            ),
            (
                "¿Qué niveles Bronce, Plata y Oro significan aquí?",
                "Niveles de confianza del dato, no premios; de bruto a accionable en tablero.",
                "¿Qué pregunta de negocio quieren que los equipos lleven al conversatorio con el régimen?",
            ),
        ],
        "puente": "Tomamos café y volvemos con academia y Constructora Bolívar en conversación.",
        "fuente": "Fuente: agenda v7, propuesta técnica EO v3 (nov 2026)",
    },
    {
        "time": "09:40",
        "title": "Conversatorio universidad y sector inmobiliario",
        "participants": "Alejandro Díaz Malagón, Constructora Bolívar · Aceleradora de Transformación, Gideon Blaauw",
        "asks": "Gideon -> academia y corporación",
        "viene": "Lanzamiento: nicho, régimen, paisaje y motor del Datalab.",
        "lleva": "Problema del corporativo que digitalización y sandbox ilustran.",
        "turns": [
            (
                "¿Qué cambio institucional pide el sector inmobiliario cuando habla de transformación?",
                "Aprender a decidir con evidencia antes de escalar obra o servicios.",
                "¿Dónde ve Bolívar el límite entre innovar y portar el régimen existente?",
            ),
            (
                "Alejandro, ¿qué puente académico necesita un adoptante del régimen?",
                "Intermediario que registra el cruce sin abrir otro ambiente de selección.",
                "¿Qué pregunta concreta le dejarían a Agrometers sobre competitividad territorial?",
            ),
            (
                "Constructora Bolívar: ¿qué resultado comprarían si la startup lo demuestra en Plata u Oro?",
                "Indicadores de sostenibilidad integrados al modelo de negocio, no solo pilotos aislados.",
                "¿Qué no prometen hoy en materia de territorio piloto del Observatorio?",
            ),
            (
                "¿Cómo se relaciona esto con los equipos estudiantiles que empiezan en bronce?",
                "El régimen necesita ver trazabilidad; ellos empiezan con WhatsApp y hojas de cálculo.",
                "¿Qué les pedirían como primer paso de madurez antes del mediodía?",
            ),
        ],
        "puente": "Enrique Medina conecta digitalización real con exportación y certificación.",
        "fuente": "Fuente: agenda v7, Canva 23 nov, reunión 23 nov",
    },
    {
        "time": "09:55",
        "title": "Conversatorio: digitalización como habilitador para la competitividad del territorio",
        "participants": "Enrique Medina (Agrometers); conversación con Gideon",
        "asks": "Gideon -> Enrique",
        "viene": "Conversatorio Bolívar: adopción en el régimen corporativo.",
        "lleva": "Puente sectorial hacia el caso urbano Air4U.",
        "turns": [
            (
                "Enrique, ¿qué NO es digitalizar para usted?",
                "No es tener correo o una app; es habilitador de competitividad real en el territorio.",
                "¿Qué dato satelital o de agua cambió una decisión de exportación?",
            ),
            (
                "¿Cómo explica la palma exportando a Europa ante exigencias de deforestación?",
                "Hay que demostrar trazabilidad territorial con métodos citables, no narrativa.",
                "¿Qué lección llevan los mentores cuando revisan mapas de calor de los equipos?",
            ),
            (
                "¿Dónde ve el sensor y la imagen de la Tierra en el sector agro?",
                "Niveles de agua, cobertura y certificación cruzan satélite con decisión de campo.",
                "¿Qué pregunta dejaría listo para el sandbox urbano de las diez cinco?",
            ),
            (
                "Usted también es jurado: ¿qué mirará en la madurez de datos al final del día?",
                "Integración del dato al modelo de negocio, no solo visualización bonita.",
                "¿Cómo conecta lo rural con calidad del aire en ciudades como Bogotá?",
            ),
            (
                "¿Qué expectativa tiene de los catorce equipos Externado?",
                "Muchos en bronce; el reto es subir grada con una pregunta de negocio clara.",
                "¿Qué historia quiere oír en los pitches de las cuatro de la tarde?",
            ),
        ],
        "puente": "Air4U muestra el nicho urbano: hacer visible lo invisible.",
        "fuente": "Fuente: agenda v7, nota agenda 23 nov",
    },
    {
        "time": "10:05",
        "title": "Data sandbox de innovación (1/3): presentación Air4U",
        "participants": "Miguel Ángel Rozo, Sebastián Forero (Air4U)",
        "asks": "Gideon -> Air4U",
        "viene": "Agrometers: digitalización y competitividad territorial.",
        "lleva": "Problema y valor que la demo de capas probará.",
        "turns": [
            (
                "Miguel, ¿por qué arrancar con la calidad del aire del fin de semana en Bogotá?",
                "El aire volvió a la conversación pública; es el momento de mostrar oportunidad, no solo alerta.",
                "¿Cómo presentan su cifra de reducción del 14% de partículas como afirmación de Air4U, no como dato oficial?",
            ),
            (
                "¿A quién venden aire limpio y por qué les importa el dato?",
                "Hospitales, farmacéuticas y cannabis; decisiones de salud exigen trazas verificables.",
                "¿Qué significa «hacer visible lo invisible» en una frase para los equipos?",
            ),
            (
                "¿Por qué en tono positivo de mercado y no de catástrofe?",
                "El cliente compra capacidad de decidir; el miedo solo no sostiene contrato.",
                "¿Qué pedirían a un equipo que copie su estructura de tablero?",
            ),
            (
                "¿Cómo se ubican en nicho frente al régimen urbano?",
                "Oferta que necesita protección mientras escala en entornos regulados.",
                "¿Qué capa de datos mostrarán en vivo en la siguiente franja?",
            ),
        ],
        "puente": "Pasamos a la demo en vivo: tres capas como escalera de confianza.",
        "fuente": "Fuente: agenda v7, revisión demo 23 nov",
    },
    {
        "time": "10:10",
        "title": "Data sandbox de innovación (2/3): demo en vivo Air4U",
        "participants": "Air4U (Miguel Ángel Rozo, Sebastián Forero)",
        "asks": "Gideon -> Air4U",
        "viene": "Pitch Air4U: problema urbano y clientes sensibles.",
        "lleva": "Modelo concreto para Hoja 4 de los equipos.",
        "turns": [
            (
                "¿Qué muestra la capa Bronce frente a datos crudos en el mapa?",
                "Entrada cruda: lecturas sin limpiar que aún no responden una pregunta de negocio.",
                "¿Qué decide el monitor cuando ve solo bronce en un equipo?",
            ),
            (
                "¿Qué cambia al pasar a Plata en la demo?",
                "Estructura que responde una pregunta; vacíos en blanco, no en cero.",
                "¿Cómo explican que medalla no es premiación sino confianza?",
            ),
            (
                "¿Qué hace distinta la capa Oro en pantalla?",
                "Dato procesado accionable: el tablero lee solo listo para decidir.",
                "¿Qué copiarían los equipos del ejemplo de clínica en Bogotá del material guía?",
            ),
            (
                "Si falla la red: ¿qué tres láminas de respaldo mantienen el hilo pedagógico?",
                "Misma escalera en estático: dónde, qué y decisión en diez segundos.",
                "¿Qué pregunta dejan para el conversatorio con un adoptante corporativo?",
            ),
            (
                "¿Cuánto tiempo queda Sebastián para la capa que más sorprende al jurado?",
                "Priorizamos la transición Plata->Oro porque ahí se ve integración al negocio.",
                "¿Cómo invitan a los mentores a usar esto en el bloque de las once?",
            ),
        ],
        "puente": "Conversatorio Air4U y adoptante potencial en indicadores de sostenibilidad.",
        "fuente": "Fuente: agenda v7, revisión demo 23 nov",
    },
    {
        "time": "10:20",
        "title": "Data sandbox de innovación (3/3): conversatorio Air4U y farmacéutica",
        "participants": "Air4U, Óscar (Apix Pharma), Gideon Blaauw",
        "asks": "Gideon -> startup y adoptante",
        "viene": "Demo: tres capas y tablero ejemplo.",
        "lleva": "Modelo de integración dato-negocio para instrucciones.",
        "turns": [
            (
                "¿Qué busca un farmacéutico cuando habla de aire limpio con una startup?",
                "Cumplir ODS 13 en planta con evidencia que aguanta auditoría.",
                "Si Apix no está: ¿qué pregunta de adoptante queda en la sala?",
            ),
            (
                "Air4U: ¿qué ofrece como producto de cliente, no solo sandbox?",
                "Entrada de solo lectura con trazas; el escudo del sandbox abre la puerta.",
                "¿Qué rol juega el Protector frente al Adoptante en este caso?",
            ),
            (
                "Óscar, ¿qué dato mínimo necesita antes de firmar interés?",
                "Serie consistente en Plata que responda una decisión semanal en planta.",
                "¿Cómo se vería el puente de valor en Hoja 4 para este par?",
            ),
            (
                "¿Qué lección llevan los catorce equipos sobre indicadores de sostenibilidad?",
                "Conectar startup con corporativo es historia de confianza escalonada, no salto a Oro.",
                "¿Qué error común quieren evitar en el bloque de trabajo?",
            ),
        ],
        "puente": "Instrucciones y arranque: reglas, embudo y mentores.",
        "fuente": "Fuente: agenda v7, nota agenda 23 nov",
    },
    {
        "time": "10:45",
        "title": "Instrucciones y arranque del datatón",
        "participants": "Gideon Blaauw, monitores del Datalab (presentación de mentores incluida)",
        "asks": "Gideon -> equipos; mentores -> equipos",
        "viene": "Sandbox: integración dato-negocio con Air4U.",
        "lleva": "Reglas, embudo catorce a seis a tres y pregunta núcleo por equipo.",
        "turns": [
            (
                "¿Cuál es el criterio principal para los seis finalistas?",
                "Madurez de datos: qué tan lejos están de responder su pregunta de negocio.",
                "¿Por qué los monitores preseleccionan y el jurado delibera después?",
            ),
            (
                "¿Qué significa Bronce, Plata y Oro para los premios del día?",
                "Son niveles de confianza, no medallas de ganador; todos reciben certificado.",
                "¿Qué herramientas pueden usar sin perder trazabilidad?",
            ),
            (
                "¿Qué hojas del paquete recorren hoy en orden?",
                "Paso cero lienzo, mapa de calor dónde, flujo y medallion qué, valor, tablero y pitch.",
                "¿Qué datos pueden usar además de los propios?",
            ),
            (
                "Mentores: ¿cuál es su superpoder hoy?",
                "Captura, limpieza y organización; no somos expertos de cada sector.",
                "¿Cómo se presentan Arnold, Daniel, Andrés, Camilo y el equipo técnico?",
            ),
            (
                "¿Qué pregunta núcleo debe salir de esta sala a las once?",
                "¿Debe [acción] antes de [cuándo] para un usuario concreto?",
                "¿Dónde quedan Air4U si hay duda de modelo de negocio?",
            ),
        ],
        "puente": "Bloque uno: lienzo y mapa de calor con monitores.",
        "fuente": "Fuente: agenda v7, mentoría 23 nov, inventario paquete equipos",
    },
    {
        "time": "11:00",
        "title": "Trabajo de equipos con monitores (bloque 1)",
        "participants": "Catorce equipos Externado, cinco mentores, apoyo Air4U",
        "asks": "Monitores -> equipos; Gideon circula",
        "viene": "Instrucciones: criterio madurez y hoja cero.",
        "lleva": "Mapa de calor iniciado y primer nivel en escalera.",
        "turns": [
            (
                "Equipo, ¿qué bloque del lienzo tiene hoy el dato más caliente?",
                "Suele ser ingresos o relación con clientes en una hoja Excel o chat.",
                "¿Dónde marcarían D1, D2 y D3 en el mapa sin inventar fuentes?",
            ),
            (
                "¿El dato es suyo, abierto o sintético y lo pueden declarar?",
                "Muchos mezclan gobierno abierto con encuesta propia; hay que etiquetar.",
                "¿Hay datos personales o confidenciales que obliguen a anonimizar?",
            ),
            (
                "Monitor: ¿qué ve en bronce que debe quedarse en bronce por ahora?",
                "WhatsApp y fotos sin estructura; no forzar Oro sin paso intermedio.",
                "¿Qué pregunta de flujo A1-A15 abre mejor el camino a Plata?",
            ),
            (
                "Air4U al pasar: ¿qué analogía de negocio sirve a este equipo?",
                "Usuario con decisión semanal y panel de diez segundos.",
                "¿Qué pide el mentor como entrega antes del almuerzo?",
            ),
            (
                "¿Cómo documentan vacíos en blanco y no en cero?",
                "Una celda vacía no es ausencia de dato; es honestidad metodológica.",
                "¿Qué señal de madurez esperan los monitores a las doce y media?",
            ),
        ],
        "puente": "Almuerzo con mesa hélice para invitados y networking abierto.",
        "fuente": "Fuente: agenda v7, mentoría 23 nov",
    },
    {
        "time": "12:30",
        "title": "Almuerzo y networking",
        "participants": "Equipos libres; mesa invitados (EmprenderMás, APC, RAP, Apix, Air4U, Enrique, Alejandro, CTH)",
        "asks": "Gideon -> mesa invitados",
        "viene": "Bloque 1: mapas de calor y bronce documentado.",
        "lleva": "Conexiones hélice y energía para bloque 2.",
        "turns": [
            (
                "En la mesa hélice: ¿qué pregunta territorio-empresa quedó sin respuesta esta mañana?",
                "Suele ser quién adopta primero cuando la evidencia aún está en Plata.",
                "¿Qué actor se ofreció a revisar un tablero en noventa días?",
            ),
            (
                "¿Qué historia de cooperación internacional resonó en el panel?",
                "Presión de trazabilidad que no puede quedarse solo en discurso.",
                "¿Cómo la traducen a un nicho que necesita protección?",
            ),
            (
                "Equipos en circulación: ¿qué dato les falta y dónde lo buscarían después de comer?",
                "Muchos piden IDEAM o registros sectoriales citables.",
                "¿A quién les recomiendan preguntar en la mesa de invitados?",
            ),
            (
                "¿Qué conversación informal acerca al Observatorio sin filtrar documentos internos?",
                "Hablamos de lentes y fases, no de borradores no publicados.",
                "¿Qué puente lanzan al bloque de preparación del pitch?",
            ),
        ],
        "puente": "Bloque dos: subir grada, tablero y ensayo de cinco minutos.",
        "fuente": "Fuente: agenda v7, nota agenda 23 nov",
    },
    {
        "time": "13:30",
        "title": "Trabajo de equipos y preparación del pitch (bloque 2)",
        "participants": "Equipos y mentores",
        "asks": "Monitores -> equipos",
        "viene": "Almuerzo: contactos y claridad de brechas de dato.",
        "lleva": "Seis finalistas elegidos y pitch ensayado.",
        "turns": [
            (
                "¿Qué sube este equipo de Plata hacia Oro antes de las cuatro?",
                "Una respuesta trazable a una sola pregunta en tablero de una pantalla.",
                "¿Qué panel de Hoja 3 ya tiene número firme solo con Plata?",
            ),
            (
                "Monitor: ¿quiénes van en el grupo de seis según madurez vista?",
                "Preselección por integración al lienzo, no por empaque visual.",
                "¿Qué equipo aún confunde medalla con premio?",
            ),
            (
                "¿Cómo arman Hoja 5 en cinco minutos?",
                "Problema, datos, tablero, impacto y próximo paso a treinta días.",
                "¿Qué pedirán para subir grada en treinta y noventa días?",
            ),
            (
                "¿Dónde está el puente de valor entre cliente, innovador y paisaje?",
                "Tres paneles en una sola pantalla; el usuario decide en diez segundos.",
                "¿Qué ensayo grabarían si tuvieran solo una toma?",
            ),
            (
                "¿Qué comunican al equipo que no pase a final?",
                "Certificado igual; seguimiento en programas futuros de CleantechHUB.",
                "¿A qué hora debe estar cerrada la lista de seis?",
            ),
        ],
        "puente": "Pitches finales de los seis equipos preseleccionados.",
        "fuente": "Fuente: agenda v7, paquete equipos, mentoría 23 nov",
    },
    {
        "time": "16:00",
        "title": "Pitches finales: seis equipos preseleccionados",
        "participants": "Seis equipos, auditorio, Gideon como moderador",
        "asks": "Gideon -> equipos; equipos -> jurado",
        "viene": "Bloque 2: seis finalistas y tableros.",
        "lleva": "Evidencia para deliberación del jurado.",
        "turns": [
            (
                "Equipo en escena: ¿quién es el usuario y qué decisión debe tomar esta semana?",
                "Responder en una frase antes de mostrar cualquier gráfico.",
                "¿Qué dato usaron que no estaba esta mañana en bronce?",
            ),
            (
                "¿Qué ve el usuario en diez segundos en su tablero?",
                "Línea base, delta del innovador y panorama abierto si aplica.",
                "¿Dónde mostraron vacíos honestos?",
            ),
            (
                "¿Cómo cuentan impacto sin inventar cifras de mercado?",
                "Cualitativo o con el número que realmente midieron.",
                "¿Cuál es el próximo paso a treinta días para subir grada?",
            ),
            (
                "Desde la sala: ¿qué repregunta afina la integración al modelo de negocio?",
                "El jurado busca que el dato sostenga ingresos, costos o relación, no solo slide.",
                "¿Qué equipo dejó mejor puente hacia Datalab dos mil veintisiete?",
            ),
            (
                "Gideon al cerrar ronda: ¿qué criterio común pidió ver en los seis?",
                "Misma escala Bronce-Oro; misma estructura de pitch.",
                "¿Cuánto tiempo de transición antes de la deliberación?",
            ),
        ],
        "puente": "Jurado a deliberar: madurez, integración y próximo paso.",
        "fuente": "Fuente: agenda v7, paquete equipos Hoja 5",
    },
    {
        "time": "16:40",
        "title": "Deliberación del jurado",
        "participants": "Enrique Medina, Alejandro Díaz Malagón, Gideon Blaauw",
        "asks": "Jurado interno; Gideon modera sala en espera",
        "viene": "Pitches: seis evidencias de tablero y negocio.",
        "lleva": "Tres ganadores para anuncio y certificados.",
        "turns": [
            (
                "¿Peso igual a madurez de datos e integración al lienzo?",
                "Sí; un tablero bonito en bronce no compite con Plata integrada.",
                "¿Hubo empate que se rompe por próximo paso creíble a treinta días?",
            ),
            (
                "¿Algún equipo sobreprometió Oro sin trazabilidad?",
                "Revisamos si la respuesta aguanta conclusión académica.",
                "¿Quién entra al Datalab de CleantechHUB en dos mil veintisiete?",
            ),
            (
                "¿Cómo se reparten conexiones de mercado entre tres ganadores?",
                "Sandbox y mentoría CTH; no es la ruta REIN de cohortes.",
                "¿Qué feedback breve llevan los tres finalistas no ganadores?",
            ),
            (
                "¿Certificados listos para todos, mentores incluidos?",
                "Sí; fotógrafo en cierre documenta el momento.",
                "¿Mensaje único si la sala pregunta por costo o acceso al programa?",
            ),
        ],
        "puente": "Cierre público: tres ganadores y entrega de certificados.",
        "fuente": "Fuente: agenda v7, mentoría 23 nov",
    },
    {
        "time": "16:50",
        "title": "Cierre: anuncio de tres ganadores y entrega de certificados",
        "participants": "Gideon Blaauw, Marlene Díaz, jurado, equipos, fotógrafo",
        "asks": "Gideon -> audiencia",
        "viene": "Deliberación: tres ganadores y criterio aplicado.",
        "lleva": "Cierre del loop hacia Observatorio fase piloto y Earth Data Week.",
        "turns": [
            (
                "¿Cómo anuncian a los tres sin confundir niveles de confianza con premio?",
                "Ganadores entran al motor del Datalab en dos mil veintisiete; todos con certificado.",
                "¿Qué agradecemos a Externado por abrir el lienzo hoy?",
            ),
            (
                "¿Qué frase devuelve el día al macro paisaje-régimen-nicho?",
                "La colaboración se volvió capacidad verificable en al menos seis tableros.",
                "¿Qué invitación a futuro programas para quienes no ganaron?",
            ),
            (
                "¿Cómo mencionan el Observatorio sin fechas ni territorio piloto?",
                "Fase de fundamento y puente hacia piloto por lente; detalle en conversaciones privadas.",
                "¿Qué foto o momento captura el fotógrafo para memoria institucional?",
            ),
            (
                "¿Cierre con el lema del día?",
                "Observa. Actúa. Transforma. — mañana el aprendizaje sigue en cada equipo.",
                "¿Última instrucción logística antes de las cinco en punto?",
            ),
        ],
        "puente": "Fin del evento; continuidad en Datalab y seguimiento a equipos.",
        "fuente": "Fuente: agenda v7, propuesta EO v3, notas 23 nov",
    },
]


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def turn_html(turns: list[tuple[str, str, str]]) -> str:
    parts = []
    for p, a, r in turns:
        parts.append(
            f'<div class="turn"><p class="pregunta">Pregunta: {esc(p)}</p>'
            f'<p class="anticipada">[{esc(a)}]</p>'
            f'<p class="repregunta">Repregunta: {esc(r)}</p></div>'
        )
    return "\n".join(parts)


def space_page(sp: dict, n: int) -> str:
    return f"""<section class="page" id="p{n:02d}" data-page="{n}">
  <header class="page-head">
    <div class="title-block">
      <span class="time-badge">{esc(sp['time'])}</span>
      <h1>{esc(sp['title'])}</h1>
      <p class="meta-row"><strong>Participan:</strong> {esc(sp['participants'])}</p>
      <p class="meta-row"><strong>Pregunta:</strong> {esc(sp['asks'])}</p>
    </div>
    <img class="logo" src="assets/cth-logo.png" alt="CleantechHUB">
  </header>
  <div class="strip-row">
    <div class="strip"><div class="label">Viene de</div>{esc(sp['viene'])}</div>
    <div class="strip"><div class="label">Lleva a</div>{esc(sp['lleva'])}</div>
  </div>
  <div class="turns">
    {turn_html(sp['turns'])}
  </div>
  <p class="puente"><strong>Puente</strong>{esc(sp['puente'])}</p>
  <p class="fuente">{esc(sp['fuente'])}</p>
</section>"""


THREAD_HTML = """
<div class="thread-grid">
  <div class="thread-col">
    <h3>Paisaje a programa</h3>
    <span class="thread-pill">08:30 Palabras de apertura</span>
    <span class="thread-pill">08:40 Panel ODS 13</span>
    <span class="thread-pill thread-pill--prog">09:10 Observatorio y Datalab</span>
    <span class="thread-pill">09:40 Conversatorio régimen corporativo</span>
    <span class="thread-pill">09:55 Digitalización (Agrometers)</span>
    <h3 style="margin-top:2mm">Nicho y método</h3>
    <span class="thread-pill thread-pill--nicho">10:05 Air4U presentación</span>
    <span class="thread-pill thread-pill--nicho">10:10 Demo capas en vivo</span>
    <span class="thread-pill thread-pill--nicho">10:20 Air4U y adoptante</span>
    <span class="thread-pill thread-pill--work">10:45 Instrucciones y mentores</span>
    <span class="thread-pill thread-pill--work">11:00 Bloque 1 con monitores</span>
    <span class="thread-pill">12:30 Almuerzo y mesa hélice</span>
    <span class="thread-pill thread-pill--work">13:30 Bloque 2 y pitch</span>
    <span class="thread-pill thread-pill--prog">16:00 Pitches (6 equipos)</span>
    <span class="thread-pill">16:40 Deliberación jurado</span>
    <span class="thread-pill thread-pill--prog">16:50 Cierre y certificados</span>
  </div>
  <div class="thread-col">
    <h3>Lentes MLP</h3>
    <article class="thread-note"><strong>Paisaje</strong>Presiones territoriales y cooperación (panel).</article>
    <article class="thread-note"><strong>Programa</strong>Observatorio, Carapulica y motor Datalab.</article>
    <article class="thread-note"><strong>Régimen</strong>Constructora Bolívar como adoptante potencial, sin piloto firmado.</article>
    <article class="thread-note"><strong>Sector</strong>Agrometers: competitividad y trazabilidad exportable.</article>
    <article class="thread-note"><strong>Nicho</strong>Air4U: lente urbana, hacer visible lo invisible.</article>
    <article class="thread-note"><strong>Método</strong>Bronce, Plata, Oro = confianza del dato.</article>
    <article class="thread-note"><strong>Equipos</strong>Catorce equipos: lienzo, mapa, tablero, pitch.</article>
    <article class="thread-note"><strong>Selección</strong>Embudo a seis finalistas y tres ganadores 2027.</article>
    <article class="thread-note"><strong>Vuelta macro</strong>Fase piloto del Observatorio y Earth Data Week.</article>
  </div>
</div>
<p class="thread-macro">Hilo: paisaje y territorio, programa Observatorio y Datalab, régimen corporativo, sector digital, nicho Air4U, método con equipos, selección y regreso al motor en 2027.</p>
"""


COVER = """<section class="page page--cover" id="p01" data-page="1">
  <div class="cover-bg"></div>
  <div class="cover-scrim"></div>
  <img class="logo" src="assets/cth-logo.png" alt="CleantechHUB">
  <div class="cover-inner">
    <p class="tagline">OBSERVA. ACTÚA. TRANSFORMA.</p>
    <h1>Datatón · preguntas por espacio</h1>
    <p class="cover-meta">Martes 24 de noviembre de 2026<br>Universidad Externado de Colombia · Auditorio Bloque I</p>
    <p class="cover-meta" style="margin-top:6mm;font-size:9.5pt;opacity:.9">Documento interno de preparación para moderación y jurado</p>
  </div>
</section>"""

THREAD_PAGE = f"""<section class="page page--thread" id="p02" data-page="2">
  <header class="page-head">
    <div class="title-block">
      <h1>Hilo conductor del día</h1>
      <p class="meta-row">De paisaje y territorio al nicho Air4U, método con equipos y vuelta al Observatorio y Datalab 2027.</p>
    </div>
    <img class="logo" src="assets/cth-logo.png" alt="CleantechHUB">
  </header>
  <div class="diagram-wrap">
    {THREAD_HTML}
  </div>
  <p class="fuente">Fuente: agenda v7, síntesis contexto 23 nov</p>
</section>"""


def main() -> None:
    css = (ROOT / "deck.css").read_text(encoding="utf-8")
    space_sections = "\n".join(space_page(sp, i + 3) for i, sp in enumerate(SPACES))
    doc = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Datatón · preguntas por espacio</title>
  <style>
{css}
  </style>
</head>
<body class="print-mode">
{COVER}
{THREAD_PAGE}
{space_sections}
</body>
</html>
"""
    OUT.write_text(doc, encoding="utf-8")
    print(f"Wrote {OUT} ({len(SPACES) + 2} pages)")


if __name__ == "__main__":
    main()
# utils/estrategias.py

ESTRATEGIAS_MANUAL = {
# INTRALABORAL
    #LIDERAZGO Y RELACIONES SOCIALES
    "Caracteristicas Liderazgo": {
        "Muy Alto": [
            {"accion": "Academia de líderes online Factores de Riesgo Psicosocial.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Coaching.", "tipo": "Prevención Terciaria", "responsable": "Desarrollo"},
            {"accion": "Mentoring (Transmisión de conocimiento).", "tipo": "Intervención Terciaria", "responsable": "Desarrollo"},
            {"accion": "Evaluación 360° líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Clara Coach Bot (Herramienta).", "tipo": "Intervención Secundaria", "responsable": "Desarrollo"},
        ],
        "Alto": [
            {"accion": "Academia de líderes online Factores de Riesgo Psicosocial.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Coaching.", "tipo": "Prevención Terciaria", "responsable": "Desarrollo"},
            {"accion": "Mentoring (Transmisión de conocimiento).", "tipo": "Intervención Terciaria", "responsable": "Desarrollo"},
            {"accion": "Evaluación 360° líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Clara Coach Bot (Herramienta).", "tipo": "Intervención Secundaria", "responsable": "Desarrollo"},
        ],
        "Medio": [
            {"accion": "Programa de nuevos líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Academia de líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Academia de líderes online Factores de Riesgo Psicosocial.", "tipo": "IntervenciónPrimaria", "responsable": "Desarrollo"},
            {"accion": "Evaluación 360° líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Entre lideres.", "tipo": "Intervención Secundaria", "responsable": "Desarrollo"},
            {"accion": "Toolkit de Comunicación (aplicacion de formación para lideres; conversaciones dificiles.", "tipo": "Intervención Secundaria", "responsable": "Desarrollo"},
        ],
        "Bajo": [
            {"accion": "Programa de nuevos líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Academia de líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Evaluación 360° líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Entre lideres.", "tipo": "Intervención Secundaria", "responsable": "Desarrollo"},
            {"accion": "Toolkit de Comunicación (aplicacion de formación para lideres; conversaciones dificiles.", "tipo": "Intervención Secundaria", "responsable": "Desarrollo"},
        ],
        "Sin Riesgo": [
            {"accion": "Programa de nuevos líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Academia de líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Evaluación 360° líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Entre lideres.", "tipo": "Intervención Secundaria", "responsable": "Desarrollo"},
            {"accion": "Toolkit de Comunicación (aplicacion de formación para lideres; conversaciones dificiles.", "tipo": "Intervención Secundaria", "responsable": "Desarrollo"},
        ]
    },

    "Relaciones Sociales": {
        "Muy Alto": [
            {"accion": "Ambientes positivos (Relaciones armoniosas).", "tipo": "Intervención Secundaria", "responsable": "Bienestar"},
            {"accion": "Prevención del consumo de sustancias psicoactivas (Actualización del  Programa, Politica, Formación para prevenir el consumo).", "tipo": "Prevención Primaria", "responsable": "SST"},
            {"accion": "Necesidades de aprendizaje para los equipos en diferentes habilidades segun resultados de cada bateria.", "tipo": "Intervención Secundaria", "responsable": "Formación"},
        ],
        "Alto": [
            {"accion": "Ambientes positivos (Relaciones armoniosas).", "tipo": "Intervención Secundaria", "responsable": "Bienestar"},
            {"accion": "Prevención del consumo de sustancias psicoactivas (Actualización del  Programa, Politica, Formación para prevenir el consumo).", "tipo": "Prevención Primaria", "responsable": "SST"},
            {"accion": "Necesidades de aprendizaje para los equipos en diferentes habilidades segun resultados de cada bateria.", "tipo": "Intervención Secundaria", "responsable": "Formación"},
        ],
        "Medio": [
            {"accion": "Ambientes positivos (Relaciones armoniosas).", "tipo": "Intervención Secundaria", "responsable": "Bienestar"},
            {"accion": "Prevención del consumo de sustancias psicoactivas (Actualización del  Programa, Politica, Formación para prevenir el consumo).", "tipo": "Prevención Primaria", "responsable": "SST"},
            {"accion": "Programa de nuevos líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Academia de líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Prevención del consumo de sustancias psicoactivas (Pruebas aleatorias).", "tipo": "Prevención Terciaria", "responsable": "SST"},
        ],
        "Bajo": [   
            {"accion": "Prevención del consumo de sustancias psicoactivas (Actualización del  Programa, Politica, Formación para prevenir el consumo).", "tipo": "Prevención Primaria", "responsable": "SST"},
            {"accion": "Programa de nuevos líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Academia de líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Prevención del consumo de sustancias psicoactivas (Pruebas aleatorias).", "tipo": "Prevención Terciaria", "responsable": "SST"},
        ],
        "Sin Riesgo": [
            {"accion": "Prevención del consumo de sustancias psicoactivas (Actualización del  Programa, Politica, Formación para prevenir el consumo).", "tipo": "Prevención Primaria", "responsable": "SST"},
            {"accion": "Programa de nuevos líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Academia de líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Prevención del consumo de sustancias psicoactivas (Pruebas aleatorias).", "tipo": "Prevención Terciaria", "responsable": "SST"},
        ]
    },

    "Retroal. Desempeño": {
        "Muy Alto": [
            {"accion": "Academia de líderes online Factores de Riesgo Psicosocial.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"}, 
            {"accion": "Coaching", "tipo": "Prevención Terciaria", "responsable": "Desarrollo"},
            {"accion": "Gestión del desempeño y productividad", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
        ],
        "Alto": [
            {"accion": "Academia de líderes online Factores de Riesgo Psicosocial.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"}, 
            {"accion": "Coaching", "tipo": "Prevención Terciaria", "responsable": "Desarrollo"},
            {"accion": "Gestión del desempeño y productividad", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
        ],
        "Medio": [
            {"accion": "Programa de nuevos líderes", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Academia de líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Academia de líderes online Factores de Riesgo Psicosocial.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},           
            {"accion": "Gestión del desempeño y productividad", "tipo": "Intervención Primaria", "responsable": "Desarrollo"}
        ],
        "Bajo": [   
            {"accion": "Programa de nuevos líderes", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Academia de líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Gestión del desempeño y productividad", "tipo": "Intervención Primaria", "responsable": "Desarrollo"}
        ],
        "Sin Riesgo": [
            {"accion": "Programa de nuevos líderes", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Academia de líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Gestión del desempeño y productividad", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
        ]
    },

    "Relación colaboradores": {
        "Muy Alto": [
            {"accion": "Ambientes positivos (Relaciones armoniosas).", "tipo": "Intervención Secundaria", "responsable": "Bienestar"}, 
            {"accion": "Academia de líderes online Factores de Riesgo Psicosocial.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},  
            {"accion": "Coaching", "tipo": "Prevención Terciaria", "responsable": "Desarrollo"},
            {"accion": "Mentoring (Transmisión de conocimiento)", "tipo": "Prevención Terciaria", "responsable": "Desarrollo"},
            {"accion": "Gestión del desempeño y productividad", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
        ],
        "Alto": [
            {"accion": "Ambientes positivos (Relaciones armoniosas).", "tipo": "Intervención Secundaria", "responsable": "Bienestar"}, 
            {"accion": "Academia de líderes online Factores de Riesgo Psicosocial.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},  
            {"accion": "Coaching", "tipo": "Prevención Terciaria", "responsable": "Desarrollo"},
            {"accion": "Mentoring (Transmisión de conocimiento)", "tipo": "Prevención Terciaria", "responsable": "Desarrollo"},
            {"accion": "Gestión del desempeño y productividad", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
        ],
        "Medio": [
            {"accion": "Programa de nuevos líderes", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Academia de líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Academia de líderes online Factores de Riesgo Psicosocial.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},           
            {"accion": "Gestión del desempeño y productividad", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Toolkit de Comunicación (aplicacion de formación para lideres; conversaciones dificiles", "tipo": "Intervención Secundaria", "responsable": "Desarrollo"},
        ],
        "Bajo": [   
            {"accion": "Programa de nuevos líderes", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Academia de líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Gestión del desempeño y productividad", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Toolkit de Comunicación (aplicacion de formación para lideres; conversaciones dificiles", "tipo": "Intervención Secundaria", "responsable": "Desarrollo"},
        ],
        "Sin Riesgo": [
            {"accion": "Programa de nuevos líderes", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Academia de líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Gestión del desempeño y productividad", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Toolkit de Comunicación (aplicacion de formación para lideres; conversaciones dificiles", "tipo": "Intervención Secundaria", "responsable": "Desarrollo"},
        ]
    },

    # CONTROL SOBRE EL TRABAJO

        "e Control y autonomia sobre el trabajo": {
        "Muy Alto": [
            {"accion": "Academia de líderes online Factores de Riesgo Psicosocial.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},  
            {"accion": "Reinducción del cargo", "tipo": "Intervención Secundaria", "responsable": "Formación"},
            {"accion": "Gestión del desempeño y productividad", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
        ],
        "Alto": [
            {"accion": "Academia de líderes online Factores de Riesgo Psicosocial.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},  
            {"accion": "Reinducción del cargo", "tipo": "Intervención Secundaria", "responsable": "Formación"},
            {"accion": "Gestión del desempeño y productividad", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
        ],
        "Medio": [
            {"accion": "Programa de nuevos lideres.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},  
            {"accion": "Academia de líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},  
            {"accion": "Academia de líderes online Factores de Riesgo Psicosocial.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},  
            {"accion": "Reinducción del cargo", "tipo": "Intervención Secundaria", "responsable": "Formación"},
            {"accion": "Gestión del desempeño y productividad", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
        ],
        "Bajo": [   
            {"accion": "Programa de nuevos líderes", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Academia de líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Gestión del desempeño y productividad", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
        ],
        "Sin Riesgo": [
            {"accion": "Programa de nuevos líderes", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Academia de líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Gestión del desempeño y productividad", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
        ]
    },

    "Oportunidades para el desarrollo": {
        "Muy Alto": [
            {"accion": "Necesidades de aprendizaje para los equipos en diferentes habilidades segun resultados de cada bateria", "tipo": "Intervención Secundaria", "responsable": "Formación"},
        ],
        "Alto": [
            {"accion": "Necesidades de aprendizaje para los equipos en diferentes habilidades segun resultados de cada bateria", "tipo": "Intervención Secundaria", "responsable": "Formación"},
        ]
    },

    "Participación y manejo del cambio": {
        "Muy Alto": [
            {"accion": "Academia de líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},  
            {"accion": "Academia de líderes online Factores de Riesgo Psicosocial.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},  
            {"accion": "Gestión del cambio para proyectos de la Organización (comunica, sensibiliza, forma  y realiza seguimiento)", "tipo": "Intervención Primaria", "responsable": "Gestión del Cambio"},
            {"accion": "Programa Humanización", "tipo": "Intervención Terciaria", "responsable": "Dirección Experiencia"},
        ],
        "Alto": [
            {"accion": "Academia de líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},  
            {"accion": "Academia de líderes online Factores de Riesgo Psicosocial.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},  
            {"accion": "Gestión del cambio para proyectos de la Organización (comunica, sensibiliza, forma  y realiza seguimiento)", "tipo": "Intervención Primaria", "responsable": "Gestión del Cambio"},
            {"accion": "Programa Humanización", "tipo": "Intervención Terciaria", "responsable": "Dirección Experiencia"},
        ],
        "Medio": [
            {"accion": "Programa de nuevos líderes", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Academia de líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},  
            {"accion": "Academia de líderes online Factores de Riesgo Psicosocial.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},  
            {"accion": "Gestión del cambio para proyectos de la Organización (comunica, sensibiliza, forma  y realiza seguimiento)", "tipo": "Intervención Primaria", "responsable": "Gestión del Cambio"},
            {"accion": "Programa Humanización", "tipo": "Intervención Terciaria", "responsable": "Dirección Experiencia"},
        ],
        "Bajo": [   
            {"accion": "Programa de nuevos líderes", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Academia de líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Gestión del cambio para proyectos de la Organización (comunica, sensibiliza, forma  y realiza seguimiento)", "tipo": "Intervención Primaria", "responsable": "Gestión del Cambio"},
            {"accion": "Programa Humanización", "tipo": "Intervención Terciaria", "responsable": "Diseño Organizacional"},
        ],
        "Sin Riesgo": [
            {"accion": "Programa de nuevos líderes", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Academia de líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Gestión del cambio para proyectos de la Organización (comunica, sensibiliza, forma  y realiza seguimiento)", "tipo": "Intervención Primaria", "responsable": "Gestión del Cambio"},
            {"accion": "Programa Humanización", "tipo": "Intervención Terciaria", "responsable": "Diseño Organizacional"},
        ]
    },

    "Claridad de Rol": {
        "Muy Alto": [
            {"accion": "Academia de líderes online Factores de Riesgo Psicosocial.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},  
            {"accion": "Reinducción del cargo.", "tipo": "Intervención Secundaria", "responsable": "Formación"},
            {"accion": "Gestión del desempeño y productividad", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
        ],
        "Alto": [
            {"accion": "Academia de líderes online Factores de Riesgo Psicosocial.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},  
            {"accion": "Reinducción del cargo.", "tipo": "Intervención Secundaria", "responsable": "Formación"},
            {"accion": "Gestión del desempeño y productividad", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
        ],
        "Medio": [
            {"accion": "Programa de nuevos líderes", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Academia de líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},  
            {"accion": "Inducción keralty.", "tipo": "Intervención Secundaria", "responsable": "Formación"},  
            {"accion": "Gestión del desempeño y productividad", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
        ],
        "Bajo": [   
            {"accion": "Programa de nuevos líderes", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Academia de líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},  
            {"accion": "Inducción keralty.", "tipo": "Intervención Secundaria", "responsable": "Formación"},  
            {"accion": "Gestión del desempeño y productividad", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
        ],
        "Sin Riesgo": [
            {"accion": "Programa de nuevos líderes", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
            {"accion": "Academia de líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},  
            {"accion": "Inducción keralty.", "tipo": "Intervención Secundaria", "responsable": "Formación"},  
            {"accion": "Gestión del desempeño y productividad", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
        ]
    },

    "Capacitación": {
        "Muy Alto": [
            {"accion": "Necesidades de aprendizaje para los equipos en diferentes habilidades segun resultados de cada bateria.", "tipo": "Intervención Secundaria", "responsable": "Formación"},  
            {"accion": "Programar espacios para realizar capacitaciones", "tipo": "Intervención Secundaria", "responsable": "Formación"},
        ],
        "Alto": [
            {"accion": "Necesidades de aprendizaje para los equipos en diferentes habilidades segun resultados de cada bateria.", "tipo": "Intervención Secundaria", "responsable": "Formación"},  
            {"accion": "Programar espacios para realizar capacitaciones", "tipo": "Intervención Secundaria", "responsable": "Formación"},
        ],
        "Medio": [
            {"accion": "Necesidades de aprendizaje para los equipos en diferentes habilidades segun resultados de cada bateria.", "tipo": "Intervención Secundaria", "responsable": "Formación"},  
            {"accion": "Programar espacios para realizar capacitaciones", "tipo": "Intervención Secundaria", "responsable": "Formación"},
        ],
        "Bajo": [   
            {"accion": "Necesidades de aprendizaje para los equipos en diferentes habilidades segun resultados de cada bateria.", "tipo": "Intervención Secundaria", "responsable": "Formación"},  
        ],
        "Sin Riesgo": [
            {"accion": "Necesidades de aprendizaje para los equipos en diferentes habilidades segun resultados de cada bateria.", "tipo": "Intervención Secundaria", "responsable": "Formación"},  
        ]
    },

    # DEMANDAS DEL TRABAJO
    
    "Demandas cuantitativas": {
        "Muy Alto": [
            {"accion": "Formación de manejo eficaz del tiempo", "tipo": "Intervención Secundaria", "responsable": "Formación"},  
            {"accion": "Gestión de cargas de trabajo; Controlar la sobrecarga cuantitativa y la mental derivada de ciertas tareas ", "tipo": "Intervención Secundaria", "responsable": "Diseño Organizacional"},
            {"accion": "Evaluacion de jornadas de turnos en mallas  FATIGA", "tipo": "Intervención Secundaria", "responsable": "Diseño Organizacional"},  
            {"accion": "Analisis de Cargo  según su perfil existente (novedades son reportadas al negocio)", "tipo": "Intervención Secundaria", "responsable": "Diseño Organizacional"},  
        ],
        "Alto": [
            {"accion": "Formación de manejo eficaz del tiempo", "tipo": "Intervención Secundaria", "responsable": "Formación"},  
            {"accion": "Gestión de cargas de trabajo; Controlar la sobrecarga cuantitativa y la mental derivada de ciertas tareas ", "tipo": "Intervención Secundaria", "responsable": "Diseño Organizacional"},
            {"accion": "Evaluacion de jornadas de turnos en mallas  FATIGA", "tipo": "Intervención Secundaria", "responsable": "Diseño Organizacional"},  
            {"accion": "Analisis de Cargo  según su perfil existente (novedades son reportadas al negocio)", "tipo": "Intervención Secundaria", "responsable": "Diseño Organizacional"},
        ],
        "Medio": [
            {"accion": "Gestión de cargas de trabajo; Controlar la sobrecarga cuantitativa y la mental derivada de ciertas tareas ", "tipo": "Intervención Secundaria", "responsable": "Diseño Organizacional"},
            {"accion": "Evaluacion de jornadas de turnos en mallas  FATIGA", "tipo": "Intervención Secundaria", "responsable": "Diseño Organizacional"},  
            {"accion": "Analisis de Cargo  según su perfil existente (novedades son reportadas al negocio)", "tipo": "Intervención Secundaria", "responsable": "Diseño Organizacional"},
        ]
    },

    "Demandas de carga mental": {
        "Muy Alto": [
            {"accion": "Gestión de cargas de trabajo; Controlar la sobrecarga cuantitativa y la mental derivada de ciertas tareas ", "tipo": "Intervención Secundaria", "responsable": "Diseño Organizacional"},
        ],
        "Alto": [
            {"accion": "Gestión de cargas de trabajo; Controlar la sobrecarga cuantitativa y la mental derivada de ciertas tareas ", "tipo": "Intervención Secundaria", "responsable": "Diseño Organizacional"},
        ],
        "Medio": [
            {"accion": "Gestión de cargas de trabajo; Controlar la sobrecarga cuantitativa y la mental derivada de ciertas tareas ", "tipo": "Intervención Secundaria", "responsable": "Diseño Organizacional"},
        ]
    },

    "Demandas emocionales": {
        "Muy Alto": [
            {"accion": "Gestión emocional - Psicokeralty individual", "tipo": "Intervención Terciaria", "responsable": "Bienestar"},  
            {"accion": "Gestión emocional - Psicokeralty grupal", "tipo": "Intervención Secundaria", "responsable": "Bienestar"},  
            {"accion": "Gestión de pausas en el trabajo. Incentivando uso de la  herramienta Haria", "tipo": "Prevención Primaria", "responsable": "SST"},  
            {"accion": "Atención en crisis y primeros auxilios psicológicos (formación a brigadistas).", "tipo": "Intervención Secundaria", "responsable": "SST"},  
            {"accion": "Prevención del consumo de sustancias psicoactivas (Pruebas aleatorias)", "tipo": "Prevención Terciaria", "responsable": "SST"},  
            {"accion": "Programa Humanización.", "tipo": "Intervención Terciaria", "responsable": "Dirección Experiencia"},
        ],
        "Alto": [
            {"accion": "Gestión emocional - Psicokeralty individual", "tipo": "Intervención Terciaria", "responsable": "Bienestar"},  
            {"accion": "Gestión emocional - Psicokeralty grupal", "tipo": "Intervención Secundaria", "responsable": "Bienestar"},  
            {"accion": "Gestión de pausas en el trabajo. Incentivando uso de la  herramienta Haria", "tipo": "Prevención Primaria", "responsable": "SST"},  
            {"accion": "Atención en crisis y primeros auxilios psicológicos (formación a brigadistas).", "tipo": "Intervención Secundaria", "responsable": "SST"},  
            {"accion": "Prevención del consumo de sustancias psicoactivas (Pruebas aleatorias)", "tipo": "Prevención Terciaria", "responsable": "SST"},  
            {"accion": "Programa Humanización.", "tipo": "Intervención Terciaria", "responsable": "Dirección Experiencia"},
        ],
        "Medio": [
            {"accion": "Gestión emocional - Psicokeralty grupal", "tipo": "Intervención Secundaria", "responsable": "Bienestar"},  
            {"accion": "Gestión de pausas en el trabajo. Incentivando uso de la  herramienta Haria", "tipo": "Prevención Primaria", "responsable": "SST"},  
            {"accion": "Atención en crisis y primeros auxilios psicológicos (formación a brigadistas).", "tipo": "Intervención Secundaria", "responsable": "SST"},  
            {"accion": "Prevención del consumo de sustancias psicoactivas (Pruebas aleatorias)", "tipo": "Prevención Terciaria", "responsable": "SST"},  
        ],
        "Bajo": [   
            {"accion": "Gestión de pausas en el trabajo. Incentivando uso de la  herramienta Haria", "tipo": "Prevención Primaria", "responsable": "SST"},  
            {"accion": "Atención en crisis y primeros auxilios psicológicos (formación a brigadistas).", "tipo": "Intervención Secundaria", "responsable": "SST"},  
        ],
        "Sin Riesgo": [
            {"accion": "Gestión de pausas en el trabajo. Incentivando uso de la  herramienta Haria", "tipo": "Prevención Primaria", "responsable": "SST"},  
            {"accion": "Atención en crisis y primeros auxilios psicológicos (formación a brigadistas).", "tipo": "Intervención Secundaria", "responsable": "SST"},  
        ]
    },

    "Exigencias de responsabilidad": {
        "Muy Alto": [
            {"accion": "Reinducción del cargo.", "tipo": "Intervención Secundaria", "responsable": "Formación"},  
            {"accion": "Gestión del desempeño y productividad", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
        ],
        "Alto": [
            {"accion": "Reinducción del cargo.", "tipo": "Intervención Secundaria", "responsable": "Formación"},  
            {"accion": "Gestión del desempeño y productividad", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
        ],
        "Medio": [
            {"accion": "Reinducción del cargo.", "tipo": "Intervención Secundaria", "responsable": "Formación"},  
            {"accion": "Gestión del desempeño y productividad", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},
        ]
    },

    "Demandas ambientales y de esfuerzo fisico": {
        "Muy Alto": [
            {"accion": "Verificar si se cuenta con evaluación  Higienica (cualitativa) con HSI (Reportar) Ruido.", "tipo": "Intervención Secundaria", "responsable": "HSI"},  
            {"accion": "Verificar si se cuenta con evaluación  Higienica (cualitativa) con HSI (Reportar) Temperatura.", "tipo": "Intervención Secundaria", "responsable": "HSI"},  
            {"accion": "Verificar si se cuenta con evaluación  Higienica (cualitativa) con HSI (Reportar) Iluminación.", "tipo": "Intervención Secundaria", "responsable": "HSI"},  
            {"accion": "Taller Manipulación adecuada de cargas.", "tipo": "Intervención Secundaria", "responsable": "SST"},  
            {"accion": "Seguimiento a inspecciónes de EPP (El lider debe garantizar el uso de EPP, Verificacion del manuel del procedimiento de bioseguridad).", "tipo": "Intervención Secundaria", "responsable": "Lider"},  
            {"accion": "Verificar si se cuenta Con inspección de riesgo quimico.", "tipo": "Intervención Secundaria", "responsable": "SST"},
            {"accion": "Verificar si se cuenta Con inspección de SOL y si el informe ya fue socializado al negocio.", "tipo": "Intervención Secundaria", "responsable": "RESPON. SG SST"},
            {"accion": "Taller en autocuidado para prevenir Accidentes de Trabajo.", "tipo": "Intervención Secundaria", "responsable": "Formación"},
        ],
        "Alto": [
            {"accion": "Verificar si se cuenta con evaluación  Higienica (cualitativa) con HSI (Reportar) Ruido.", "tipo": "Intervención Secundaria", "responsable": "HSI"},  
            {"accion": "Verificar si se cuenta con evaluación  Higienica (cualitativa) con HSI (Reportar) Temperatura.", "tipo": "Intervención Secundaria", "responsable": "HSI"},  
            {"accion": "Verificar si se cuenta con evaluación  Higienica (cualitativa) con HSI (Reportar) Iluminación.", "tipo": "Intervención Secundaria", "responsable": "HSI"},  
            {"accion": "Taller Manipulación adecuada de cargas.", "tipo": "Intervención Secundaria", "responsable": "SST"},  
            {"accion": "Seguimiento a inspecciónes de EPP (El lider debe garantizar el uso de EPP, Verificacion del manuel del procedimiento de bioseguridad).", "tipo": "Intervención Secundaria", "responsable": "Lider"},  
            {"accion": "Verificar si se cuenta Con inspección de riesgo quimico.", "tipo": "Intervención Secundaria", "responsable": "SST"},
            {"accion": "Verificar si se cuenta Con inspección de SOL y si el informe ya fue socializado al negocio.", "tipo": "Intervención Secundaria", "responsable": "RESPON. SG SST"},
            {"accion": "Taller en autocuidado para prevenir Accidentes de Trabajo.", "tipo": "Intervención Secundaria", "responsable": "Formación"},
        ],
        "Medio": [
            {"accion": "Verificar si se cuenta con evaluación  Higienica (cualitativa) con HSI (Reportar) Ruido.", "tipo": "Intervención Secundaria", "responsable": "HSI"},  
            {"accion": "Verificar si se cuenta con evaluación  Higienica (cualitativa) con HSI (Reportar) Temperatura.", "tipo": "Intervención Secundaria", "responsable": "HSI"},  
            {"accion": "Verificar si se cuenta con evaluación  Higienica (cualitativa) con HSI (Reportar) Iluminación.", "tipo": "Intervención Secundaria", "responsable": "HSI"},  
            {"accion": "Taller Manipulación adecuada de cargas.", "tipo": "Intervención Secundaria", "responsable": "SST"},  
            {"accion": "Seguimiento a inspecciónes de EPP (El lider debe garantizar el uso de EPP, Verificacion del manuel del procedimiento de bioseguridad).", "tipo": "Intervención Secundaria", "responsable": "Lider"},  
            {"accion": "Verificar si se cuenta Con inspección de riesgo quimico.", "tipo": "Intervención Secundaria", "responsable": "SST"},
            {"accion": "Verificar si se cuenta Con inspección de SOL y si el informe ya fue socializado al negocio.", "tipo": "Intervención Secundaria", "responsable": "RESPON. SG SST"},
            {"accion": "Taller en autocuidado para prevenir Accidentes de Trabajo.", "tipo": "Intervención Secundaria", "responsable": "Formación"},
        ]
    },

    "Demandas de jornada laboral": {
        "Muy Alto": [
            {"accion": "Gestión de pausas en el trabajo. Incentivando uso de la  herramienta Haria.", "tipo": "Prevención Primaria", "responsable": "SST"},  
            {"accion": "Formación de manejo eficaz del tiempo.", "tipo": "Intervención Secundaria", "responsable": "Formación"},  
            {"accion": "Gestión de cargas de trabajo; Controlar la sobrecarga cuantitativa y la mental derivada de ciertas tareas.", "tipo": "Intervención Secundaria", "responsable": "Diseño Organizacional"},
            {"accion": "Evaluacion de jornadas de turnos en mallas  FATIGA.", "tipo": "Intervención Secundaria", "responsable": "Diseño Organizacional"},
        ],
        "Alto": [
            {"accion": "Gestión de pausas en el trabajo. Incentivando uso de la  herramienta Haria.", "tipo": "Prevención Primaria", "responsable": "SST"},  
            {"accion": "Formación de manejo eficaz del tiempo.", "tipo": "Intervención Secundaria", "responsable": "Formación"},  
            {"accion": "Gestión de cargas de trabajo; Controlar la sobrecarga cuantitativa y la mental derivada de ciertas tareas.", "tipo": "Intervención Secundaria", "responsable": "Diseño Organizacional"},
            {"accion": "Evaluacion de jornadas de turnos en mallas  FATIGA.", "tipo": "Intervención Secundaria", "responsable": "Diseño Organizacional"},
        ],
        "Medio": [
            {"accion": "Gestión de pausas en el trabajo. Incentivando uso de la  herramienta Haria.", "tipo": "Prevención Primaria", "responsable": "SST"},     
            {"accion": "Gestión de cargas de trabajo; Controlar la sobrecarga cuantitativa y la mental derivada de ciertas tareas.", "tipo": "Intervención Secundaria", "responsable": "Diseño Organizacional"},
            {"accion": "Evaluacion de jornadas de turnos en mallas  FATIGA.", "tipo": "Intervención Secundaria", "responsable": "Diseño Organizacional"},
        ],
        "Bajo": [   
            {"accion": "Gestión de pausas en el trabajo. Incentivando uso de la  herramienta Haria.", "tipo": "Prevención Primaria", "responsable": "SST"},     
        ],
        "Sin Riesgo": [
            {"accion": "Gestión de pausas en el trabajo. Incentivando uso de la  herramienta Haria.", "tipo": "Prevención Primaria", "responsable": "SST"},     
        ]
    },

    "Consistencia de rol": {
        "Muy Alto": [
            {"accion": "Academia de líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},  
            {"accion": "Reinducción del cargo", "tipo": "Intervención Secundaria", "responsable": "Formación"},  
        ],
        "Alto": [
            {"accion": "Academia de líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},  
            {"accion": "Reinducción del cargo", "tipo": "Intervención Secundaria", "responsable": "Formación"},  
        ],
        "Medio": [
            {"accion": "Programa de nuevos líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},  
            {"accion": "Academia de líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},  
            {"accion": "Academia de líderes Online Factores de riesgo psicosocial", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},  
        ],
        "Bajo": [   
            {"accion": "Programa de nuevos líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},  
            {"accion": "Academia de líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},  
            {"accion": "Academia de líderes Online Factores de riesgo psicosocial", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},   
        ],
        "Sin Riesgo": [
            {"accion": "Programa de nuevos líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},  
            {"accion": "Academia de líderes.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},  
            {"accion": "Academia de líderes Online Factores de riesgo psicosocial", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},     
        ]
    },

    "Influencia sobre el entorno extra": {
        "Muy Alto": [
            {"accion": "Prevención del consumo de sustancias psicoactivas (Actualización del  Programa, Politica, Formación para prevenir el consumo).", "tipo": "Intervención Primaria", "responsable": "SST"},  
            {"accion": "Prevención del consumo de sustancias psicoactivas (Pruebas aleatorias)", "tipo": "Prevención Terciaria", "responsable": "SST"},  
        ],
        "Alto": [
            {"accion": "Prevención del consumo de sustancias psicoactivas (Actualización del  Programa, Politica, Formación para prevenir el consumo).", "tipo": "Intervención Primaria", "responsable": "SST"},  
            {"accion": "Prevención del consumo de sustancias psicoactivas (Pruebas aleatorias)", "tipo": "Prevención Terciaria", "responsable": "SST"},  
        ],
        "Medio": [
            {"accion": "Prevención del consumo de sustancias psicoactivas (Actualización del  Programa, Politica, Formación para prevenir el consumo).", "tipo": "Intervención Primaria", "responsable": "SST"},  
            {"accion": "Prevención del consumo de sustancias psicoactivas (Pruebas aleatorias)", "tipo": "Prevención Terciaria", "responsable": "SST"},  
        ],
        "Bajo": [   
            {"accion": "Prevención del consumo de sustancias psicoactivas (Actualización del  Programa, Politica, Formación para prevenir el consumo).", "tipo": "Intervención Primaria", "responsable": "SST"},  
        ],
        "Sin Riesgo": [
            {"accion": "Prevención del consumo de sustancias psicoactivas (Actualización del  Programa, Politica, Formación para prevenir el consumo).", "tipo": "Intervención Primaria", "responsable": "SST"},  
        ]
    },

    # RECOMPENSAS

    "Reconocimiento y compensación": {
        "Muy Alto": [
            {"accion": "Inducción Keralty", "tipo": "Intervención Secundaria", "responsable": "Formación"},   
        ],
        "Alto": [
            {"accion": "Inducción Keralty", "tipo": "Intervención Secundaria", "responsable": "Formación"},   
        ],
        "Medio": [
            {"accion": "Programa de nuevos lideres.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},  
            {"accion": "Academia de lideres.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},   
            {"accion": "Academia de lideres Online Factores de riesgo psicosocial", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},   
        ],
        "Bajo": [   
            {"accion": "Programa de nuevos lideres.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},  
            {"accion": "Academia de lideres.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},   
            {"accion": "Academia de lideres Online Factores de riesgo psicosocial", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},    
        ],
        "Sin Riesgo": [
            {"accion": "Programa de nuevos lideres.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},  
            {"accion": "Academia de lideres.", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},   
            {"accion": "Academia de lideres Online Factores de riesgo psicosocial", "tipo": "Intervención Primaria", "responsable": "Desarrollo"},     
        ]
    },

    "Recompensas de pertenencia y trabajo": {
        "Muy Alto": [
            {"accion": "Programa de reconocimiento", "tipo": "Intervención Terciaria", "responsable": "Bienestar"},   
            {"accion": "Inducción Keralty", "tipo": "Intervención Secundaria", "responsable": "Formación"},   
        ],
        "Alto": [
            {"accion": "Programa de reconocimiento", "tipo": "Intervención Terciaria", "responsable": "Bienestar"},   
            {"accion": "Inducción Keralty", "tipo": "Intervención Secundaria", "responsable": "Formación"},    
        ]
    },


}
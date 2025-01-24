from django.urls import path
from aplications.views import *
from django.conf.urls.static import static
from django.conf import settings

from aplications.views import viewsHeuristic
from aplications.views import viewsGetProblems
from aplications.views import viewsEvaluation
from aplications.views import viewsGetObservations

urlpatterns = [
    # Inicia para HeuristicCheckList
    path('HeuristicCheckList', viewsHeuristicCheckList.API_HeuristicCheckList),
    path('HeuristicCheckList/id/<int:pk>', viewsHeuristicCheckList.API_HeuristicCheckList_Details),
    # Finaliza para HeuristicCheckList

    # Inicia para HeuristicOwner
    path('owners', viewsHeuristicOwner.API_HeuristicOwner),  # Para obtener o crear HeuristicOwner
    path('owners/<int:pk>', viewsHeuristicOwner.API_HeuristicOwner_Details),  # Para obtener o actualizar HeuristicOwner por ID
    # Finaliza para HeuristicOwner

    # Inicia para HeuristicEvaluations
    path('HeuristicEvaluations', viewsHeuristicEvaluations.API_HeuristicEvaluations),
    path('HeuristicEvaluations/id/<int:pk>', viewsHeuristicEvaluations.API_HeuristicEvaluations_Details),
    # Finaliza para HeuristicEvaluations

    # Inicia para HeuristicDescriptions
    path('HeuristicDescriptions', viewsHeuristicDescriptions.API_HeuristicDescriptions),
    path('HeuristicDescriptions/id/<int:pk>', viewsHeuristicDescriptions.API_HeuristicDescriptions_Details),
    # Finaliza para HeuristicEvaluations

    # Inicia para PorcentajeCheckList
    path('PorcentajeCheckList', viewsPorcentajeCheckList.API_PorcentajeCheckList),
    path('PorcentajeCheckList/id/<int:pk>', viewsPorcentajeCheckList.API_PorcentajeCheckList_Details),
    # Finaliza para PorcentajeCheckList

    # Inicia para EvaluatorInfo
    path('evaluator_info', viewsEvaluatorInfo.API_EvaluatorInfo),
    path('evaluator_info/id/<int:pk>', viewsEvaluatorInfo.API_EvaluatorInfo_Details),
    # Finaliza para EvaluatorInfo

    # Inicia para Heuristics
    path('heuristics', viewsHeuristic.API_Heuristic), 
    path('heuristics/owner/<int:owner_id>', viewsHeuristic.API_Heuristic_By_Owner), 
    path('heuristics/id/<int:pk>', viewsHeuristic.API_Heuristic_Details), 
    # Finaliza para heuristics
    
    path('api/identifyproblems/<int:owner_id>/', viewsGetProblems.API_Get_Problems),
    path('api/getobservations/<int:owner_id>/', viewsGetObservations.API_Get_Observations),
    path('api/evaluations/<int:owner_id>/', viewsEvaluation.API_Evaluation),
    path('api/evaluations/<int:owner_id>/', viewsEvaluation.API_Evaluation_Details), 

    #////////////////////////////////////////////////////////
    # Inicia para User
    path('users/', API_User),  # Listar todos los usuarios o crear uno nuevo
    path('userData/id/<str:pk>', API_User_Details),  # Obtener o actualizar un usuario por ID
    path('userRegister/email/<str:email>', API_User_Register),  # Obtener o actualizar un usuario por email
    path('login/', API_User_Login),  # Autenticar usuario (inicio de sesión)
    # Finaliza para User

    # Inicia para DesignTest
    path('designtest/', API_DesignTest),  # Listar todas las pruebas de diseño o crear una nueva
    path('designtest/user/<int:user>/', API_DesignTests_ByUser),  # Obtener todas las pruebas de diseño por usuario
    path('designtest/test_id/<int:pk>/', API_DesignTest_Details),  # Obtener, actualizar o eliminar una prueba de diseño por su ID
    path('designtest/checkcode/<str:code>/', API_CheckCodeAvailability),  # Verificar si el código ya está en uso
    # Finaliza para DesignTest

    # Inicia para DesignQuestion
    path('heuristics/', API_GetHeuristics),  # Ruta para ver todas las heurísticas con sus subprincipios
    path('designtest/<int:test_id>/heuristics/', API_CheckHeuristics), # Ruta para verificar si la prueba tiene heurísticas
    path('designquestions/', API_AllDesignQuestions),  # Ruta para ver todas las preguntas de diseño
    path('designtest/<int:test_id>/designquestions/', API_DesignQuestions),  # Ruta para ver o crear preguntas de diseño en una prueba específica
    path('designtest/<int:test_id>/designquestions/<int:question_id>/', API_DesignQuestions_Details),  # Ruta para ver, actualizar o eliminar una pregunta de diseño específica
    # Finaliza para DesignQuestion

    # Inicia para EvaluatorAccess
    path('designtests/access/<int:evaluator_id>/', API_Access_DesignTest),  # Ruta para gestionar el acceso del evaluador a pruebas de diseño
    path('designtests/access/<int:test_id>/hide/', HIDE_Access_DesignTest),  # Ruta para ocultar una prueba de diseño para el evaluador
    path('designtests/access/<int:test_id>/show/', SHOW_Access_DesignTest),  # Ruta para mostrar una prueba de diseño oculta para el evaluador
    # Finaliza para EvaluatorAccess

    # Inicia para EvaluatorStandardResponses
    path('designtests/<int:test_id>/evaluatorstandardresponses/<int:evaluator_id>/', API_EvaluatorStandardResponse),  # Ruta para gestionar respuestas parciales del evaluador
    path('designtests/<int:test_id>/evaluatorstandardresponsesfinalize/', API_FinalizeAndGetStandardResponses),  # Ruta para finalizar y ver respuestas completas
    # Finaliza para EvaluatorStandardResponses

    # Inicia para EvaluatorHeuristicResponses
    path('designtests/<int:test_id>/evaluatorheuristicresponses/<int:evaluator_id>/', API_EvaluatorHeuristicResponse),  # Ruta para gestionar respuestas parciales del evaluador
    path('designtests/<int:test_id>/evaluatorheuristicresponsesfinalize/', API_FinalizeAndGetHeuristicResponses),  # Ruta para finalizar y ver respuestas completas
    # Finaliza para EvaluatorHeuristicResponses

    # Inicia para Screenshot
    path('capture/', CaptureScreenshotView.as_view()), # Ruta para hacer la captura del frame
    # Finaliza para Screenshot
]
# Solo se aplica en modo DEBUG para servir archivos multimedia como capturas de pantalla
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

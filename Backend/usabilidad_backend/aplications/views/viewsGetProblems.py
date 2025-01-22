from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from aplications.models import CheckList, Descriptions
import re

@api_view(['GET'])
def API_Get_Problems(request, owner_id):
    try:
        # Obtener todas las heurísticas asociadas al owner_id
        heuristics = CheckList.objects.filter(owner_id=owner_id)

        heuristics_list = []
        for heuristic in heuristics:
            heuristics_list.append({
                'H01P01': heuristic.H01P01,
                'H01P02': heuristic.H01P02,
                'H01P03': heuristic.H01P03,
                'H01P04': heuristic.H01P04,
                'H01P05': heuristic.H01P05,
                'H01P06': heuristic.H01P06,
                'H01P07': heuristic.H01P07,
                'H02P01': heuristic.H02P01,
                'H02P02': heuristic.H02P02,
                'H02P03': heuristic.H02P03,
                'H02P04': heuristic.H02P04,
                'H02P05': heuristic.H02P05,
                'H02P06': heuristic.H02P06,
                'H02P07': heuristic.H02P07,
                'H02P08': heuristic.H02P08,
                'H03P01': heuristic.H03P01,
                'H03P02': heuristic.H03P02,
                'H03P03': heuristic.H03P03,
                'H03P04': heuristic.H03P04,
                'H03P05': heuristic.H03P05,
                'H03P06': heuristic.H03P06,
                'H04P01': heuristic.H04P01,
                'H04P02': heuristic.H04P02,
                'H04P03': heuristic.H04P03,
                'H04P04': heuristic.H04P04,
                'H04P05': heuristic.H04P05,
                'H04P06': heuristic.H04P06,
                'H04P07': heuristic.H04P07,
                'H04P08': heuristic.H04P08,
                'H04P09': heuristic.H04P09,
                'H04P10': heuristic.H04P10,
                'H04P11': heuristic.H04P11,
                'H04P12': heuristic.H04P12,
                'H04P13': heuristic.H04P13,
                'H05P01': heuristic.H05P01,
                'H05P02': heuristic.H05P02,
                'H05P03': heuristic.H05P03,
                'H05P04': heuristic.H05P04,
                'H05P05': heuristic.H05P05,
                'H06P01': heuristic.H06P01,
                'H06P02': heuristic.H06P02,
                'H06P03': heuristic.H06P03,
                'H07P01': heuristic.H07P01,
                'H07P02': heuristic.H07P02,
                'H07P03': heuristic.H07P03,
                'H07P04': heuristic.H07P04,
                'H07P05': heuristic.H07P05,
                'H07P06': heuristic.H07P06,
                'H07P07': heuristic.H07P07,
                'H08P01': heuristic.H08P01,
                'H08P02': heuristic.H08P02,
                'H08P03': heuristic.H08P03,
                'H08P04': heuristic.H08P04,
                'H08P05': heuristic.H08P05,
                'H08P06': heuristic.H08P06,
                'H08P07': heuristic.H08P07,
                'H08P08': heuristic.H08P08,
                'H08P09': heuristic.H08P09,
                'H08P10': heuristic.H08P10,
                'H08P11': heuristic.H08P11,
                'H09P01': heuristic.H09P01,
                'H09P02': heuristic.H09P02,
                'H09P03': heuristic.H09P03,
                'H09P04': heuristic.H09P04,
                'H09P05': heuristic.H09P05,
                'H09P06': heuristic.H09P06,
                'H10P01': heuristic.H10P01,
                'H10P02': heuristic.H10P02,
                'H10P03': heuristic.H10P03,
                'H10P04': heuristic.H10P04,
                'H10P05': heuristic.H10P05,
                'H10P06': heuristic.H10P06,
                'H10P07': heuristic.H10P07,
                'H10P08': heuristic.H10P08,
                'H10P09': heuristic.H10P09,
            })

        # Contar las heurísticas falsas
        false_heuristics_count = {}
        for heuristics_dict in heuristics_list:
            for heuristic, value in heuristics_dict.items():
                if not value:
                    false_heuristics_count[heuristic] = false_heuristics_count.get(heuristic, 0) + 1

        # Descripciones para las heurísticas
        hi = [
            "telacreiste",
            "Visibilidad del estado del sistema",
            "Relación entre el sistema y el mundo real",
            "Control y libertad de usuario",
            "Consistencia y Estándares",
            "Prevención de Errores",
            "Minimizar la carga de memoria del usuario",
            "Flexibilidad y eficiencia de uso ",
            "Diseño estético y minimalista",
            "Ayuda al usuario para reconocer, diagnosticar y recuperarse de errores",
            "Ayuda y Documentación",
        ]
        
        response = []
        for heuristic, count in false_heuristics_count.items():
            # Obtener la descripción de la heurística
            description_obj = Descriptions.objects.filter(name=heuristic).first()
            description = description_obj.description if description_obj else "Descripción no disponible"
            
            # Asociar el nombre de la heurística con su descripción en 'hi'
            hfail = ""
            resultado = re.search(r'h(\d+)', heuristic, re.IGNORECASE)
            if resultado:
                numero_despues_de_h = resultado.group(1)
                hfail = hi[int(numero_despues_de_h)] if 0 <= int(numero_despues_de_h) < len(hi) else "Descripción no encontrada"
            
            response.append({
                "name": heuristic,
                "description": description,
                "hi": hfail,
                "incidents": count
            })

        return Response(response, status=status.HTTP_200_OK)

    except Exception as e:
        # Manejo de errores generales
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

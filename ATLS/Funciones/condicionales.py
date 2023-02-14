import cv2
import json
# VOCALES POR APARTE

def obtenerA(dedos, frame):
    font = cv2.FONT_HERSHEY_SIMPLEX
    if dedos == [1, 1, 0, 0, 0, 0]:
            cv2.rectangle(frame, (0, 0), (100, 100), (255, 255, 255), -1)
            cv2.putText(frame, 'A', (20, 80), font, 3, (0, 0, 0), 2, cv2.LINE_AA)
            
            data = {
                "valor_booleanoA": True
            }
            
            with open("info.json", "w") as f:
                 json.dump(data, f)
                 
    else:
         data = {
                "valor_booleanoA": False
            }
         with open("info.json", "w") as f:
                json.dump(data, f)
            
            
            
def obtenerE(dedos, frame):
    font = cv2.FONT_HERSHEY_SIMPLEX
    if dedos == [0, 0, 0, 0, 0, 0]:
            cv2.rectangle(frame, (0, 0), (100, 100), (255, 255,255), -1)
            cv2.putText(frame, 'E', (20, 80), font, 3, (0,0,0),2,cv2.LINE_AA)
            print("E")
            data = {
                "valor_booleanoE": True
            }
            
            with open("info.json", "w") as f:
                 json.dump(data, f)
                 
    else:
         data = {
                "valor_booleanoE": False
            }
         with open("info.json", "w") as f:
                json.dump(data, f)
             
 
            
def obtenerI(dedos, frame):
    font = cv2.FONT_HERSHEY_SIMPLEX
    if dedos == [0, 0, 1, 0, 0, 0]:
            cv2.rectangle(frame, (0, 0), (100, 100), (255, 255,255), -1)
            cv2.putText(frame, 'I', (20, 80), font, 3, (0,0,0),2,cv2.LINE_AA)
            print("I")
            data = {
                "valor_booleanoI": True
            }
            
            with open("info.json", "w") as f:
                 json.dump(data, f)
                 
    else:
         data = {
                "valor_booleanoI": False
            }
         with open("info.json", "w") as f:
                json.dump(data, f)
            
            

def obtenerO(dedos, frame):
    font = cv2.FONT_HERSHEY_SIMPLEX
    if dedos == [1, 0, 1, 0, 0, 0]:
            cv2.rectangle(frame, (0, 0), (100, 100), (255, 255,255), -1)
            cv2.putText(frame, 'O', (20, 80), font, 3, (0,0,0),2,cv2.LINE_AA)
            print("O")
            
            data = {
                "valor_booleanoO": True
            }
            
            with open("info.json", "w") as f:
                 json.dump(data, f)
                 
    else:
         data = {
                "valor_booleanoO": False
            }
         with open("info.json", "w") as f:
                json.dump(data, f)
            
            
def obtenerU(dedos, frame):
    font = cv2.FONT_HERSHEY_SIMPLEX
    if dedos == [0, 0, 0, 0, 1, 1]:
            cv2.rectangle(frame, (0, 0), (100, 100), (255, 255,255), -1)
            cv2.putText(frame, 'U', (20, 80), font, 3, (0,0,0),2,cv2.LINE_AA)
            print("U")
            
            data = {
                "valor_booleanoU": True
            }
            
            with open("info.json", "w") as f:
                 json.dump(data, f)
                 
    else:
         data = {
                "valor_booleanoU": False
            }
         with open("info.json", "w") as f:
                json.dump(data, f)
            




def condicionalesLetras(dedos, frame):
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    if dedos == [1, 1, 0, 0, 0, 0]:
            cv2.rectangle(frame, (0, 0), (100, 100), (255, 255, 255), -1)
            cv2.putText(frame, 'A', (20, 80), font, 3, (0, 0, 0), 2, cv2.LINE_AA)
            print("A")
    
    if dedos == [0, 0, 0, 0, 0, 0]:
            cv2.rectangle(frame, (0, 0), (100, 100), (255, 255,255), -1)
            cv2.putText(frame, 'E', (20, 80), font, 3, (0,0,0),2,cv2.LINE_AA)
            print("E")

    if dedos == [0, 0, 1, 0, 0, 0]:
            cv2.rectangle(frame, (0, 0), (100, 100), (255, 255,255), -1)
            cv2.putText(frame, 'I', (20, 80), font, 3, (0,0,0),2,cv2.LINE_AA)
            print("I")

    if dedos == [1, 0, 1, 0, 0, 0]:
            cv2.rectangle(frame, (0, 0), (100, 100), (255, 255,255), -1)
            cv2.putText(frame, 'O', (20, 80), font, 3, (0,0,0),2,cv2.LINE_AA)
            print("O")

    if dedos == [0, 0, 1, 0, 0, 1]:
            cv2.rectangle(frame, (0, 0), (100, 100), (255, 255,255), -1)
            cv2.putText(frame, 'U', (20, 80), font, 3, (0,0,0),2,cv2.LINE_AA)
            print("U")


    # abecedario
    return dedos
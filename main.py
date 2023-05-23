import cv2 as cv
import numpy as np
import time
from HandTracker import HandTracker

PRIMARY_COLOUR = (85, 52, 190) # BGR 0-255 , VIVA MAGENTA
PRIMARY_FONT_COLOUR = (255, 255, 255) # BGR 0-255 , VIVA MAGENTA
MUTED_PRIMARY_FONT_COLOUR = (128, 128, 128)

def preprocess(input_rgb,reshape=True):

  def process_each_image(image):
    #convert to HSV
    image = cv.cvtColor(image, cv.COLOR_RGB2HSV)
    #normalize to V
    image[:,:,2] = cv.equalizeHist(image[:,:,2])
    #convert to RGB
    image = cv.cvtColor(image, cv.COLOR_HSV2RGB)
    return image

  output = np.array([process_each_image(image) for image in input_rgb]) 
  if reshape:
    output = output.reshape(output.shape[0],-1)
  return output
def draw(input,fps:float=0.0):
    output = input

    # draw text on image
    font = cv.FONT_HERSHEY_SIMPLEX
    cv.putText(output, f'''Press q to quit''', (20, 50), font, 0.5, (255, 255, 255), 1, cv.LINE_AA)
    cv.putText(output, f'''fps : {fps:.2f}''', (20, 80), font, 0.5, (255, 255, 255), 1, cv.LINE_AA)


    return output

    
class handGesture():
    def __init__(self):
        pass
    def gestureFinder(self,image):
        pass
class nlp():
    def __init__(self):
        pass

temp_text = "lore ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation"
temp_words = temp_text.split(" ")
if __name__ == "__main__":
    print("Hello, World!")
    # init camera
    cap = cv.VideoCapture(1)
    # # init mediapipe
    tracker = HandTracker(maxHands=1)
    
    # init fps
    pTime = 0

    words = temp_words
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        output_frame = frame
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # Our operations on the frame come here
        # output_frame = preprocess(np.array([output_frame]),reshape=False)[0]
        output_frame = tracker.handsFinder(output_frame)
        lmList,handlist = np.array(tracker.positionFinder(output_frame))


        ### draw text box ###
        # draw rectangle buttom of frame
        cv.rectangle(output_frame, (0, output_frame.shape[0]-50), (output_frame.shape[1], output_frame.shape[0]), (0, 0, 0), cv.FILLED)
        
        draw_text = " ".join(words[-10:-1])
        cv.putText(output_frame, draw_text, (20, output_frame.shape[0]-20), cv.FONT_HERSHEY_SIMPLEX, 0.5, PRIMARY_FONT_COLOUR, 1, cv.LINE_AA)
        #draw last word
        text_size = cv.getTextSize(draw_text, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv.putText(output_frame, words[-1], (30+text_size[0][0], output_frame.shape[0]-20), cv.FONT_HERSHEY_SIMPLEX, 0.5, MUTED_PRIMARY_FONT_COLOUR, 1, cv.LINE_AA)
        
        
        
        # Display the resulting frame
        cv.imshow('frame', draw(output_frame,fps=fps))
        
        # cv.imshow('', draw(output_frame,fps=fps))
        if cv.waitKey(1) == ord('q'):
            break
        if cv.waitKey(1) == ord('n'):
            words = []
    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()
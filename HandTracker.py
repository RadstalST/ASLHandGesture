class HandTracker():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5,modelComplexity=1,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.modelComplex,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

        self.PRIMARY_COLOUR = (85, 52, 190) # BGR 0-255 , VIVA MAGENTA
        self.PRIMARY_FONT_COLOUR = (255, 255, 255) # BGR 0-255 , VIVA MAGENTA
    def handsFinder(self,image,draw=True):
        imageRGB = cv.cvtColor(image,cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:

                if draw:
                    self.mpDraw.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS)
        return image
    def positionFinder(self,image, handNo=0, draw=True):
        lmlist = []
        handlist = []
        if self.results.multi_hand_landmarks:
            Hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(Hand.landmark):
                h,w,c = image.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                lmlist.append([id,cx,cy])
            if draw:
                cv.circle(image,(cx,cy), 15 , (255,0,255), cv.FILLED)
                # draw bounding box
                x, y, w, h = cv.boundingRect(np.array(lmlist)[:,1:])
                offset = 50                
                # cv.rectangle(image, (x-offset, y-offset), (x + w+offset, y + h+offset), (255, 0, 255), 2)
                
                center = (x + w//2, y + h//2)
                square_size = max(w,h)
                x1 = center[0] - square_size//2 - offset
                y1 = center[1] - square_size//2 - offset
                x2 = center[0] + square_size//2 + offset
                y2 = center[1] + square_size//2 + offset
                cv.rectangle(image, (x1, y1), (x2, y2), self.PRIMARY_COLOUR, 2)
                #draw tag on bounding box
                #draw rectangle tag
                cv.rectangle(image, (x1, y1-20), (x2, y1), self.PRIMARY_COLOUR, cv.FILLED)
                cv.rectangle(image, (x1, y1-20), (x2, y1), self.PRIMARY_COLOUR, 2)
                cv.putText(image, f'''hand:{handNo}''', (x1+5, y1-5), cv.FONT_HERSHEY_SIMPLEX, 0.5, self.PRIMARY_FONT_COLOUR, 1, cv.LINE_AA)
                handlist.append((x1,y1,x2,y2))




        return lmlist,handlist
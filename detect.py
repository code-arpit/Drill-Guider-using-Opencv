import cv2 as cv

class Drill():
    def cam_detected(self, cam):
        # while True:
            w = cam.shape[1]
            h = cam.shape[0]
            detector = self.parameters()
            keypoints = detector.detect(cam)
            overlay = cam.copy()

            #targetting circle
            main_center_x = int(w/2)
            main_center_y = int(h/2)
            # print(target_y)
            # print(main_center_x)
            main_center_color_x = (255,0,0)
            main_center_color_y = (255,0,0) 
            
            for k in keypoints:
                target_x = int(k.pt[0])
                target_y = int(k.pt[1])
                cv.circle(overlay, (target_x, target_y), int(k.size/2), (255,0,0), 3)
                cv.line(overlay, (target_x-5, target_y), (target_x+5, target_y), (0,0,255), 3)
                cv.line(overlay, (target_x, target_y-5), (target_x, target_y+5), (0,0,255), 3)
                cv.line(overlay, (target_x, target_y), (main_center_x, main_center_y), (255,0,0), 2)
            
                if target_x == main_center_x and not target_y == main_center_y:
                    main_center_color_y = (0,255,0)
                    cv.circle(overlay, (target_x, target_y), int(k.size/2), (0,255,0), -1)
                
                elif not target_x == main_center_x and target_y == main_center_y:
                    main_center_color_x = (0,255,0)
                    cv.circle(overlay, (target_x, target_y), int(k.size/2), (0,255,0), -1)
                    
                elif target_y == main_center_y and target_x == main_center_x:
                    main_center_color_x = (0,255,0)
                    main_center_color_y = (0,255,0)
                    cv.circle(overlay, (target_x, target_y), int(k.size/2), (0,255,0), -1)
                else:
                    main_center_color_x = (255,0,0)         

            cv.circle(overlay, (main_center_x, main_center_y), 2, (0,255,0), -1)
            cv.line(overlay, (main_center_x-40, main_center_y), (main_center_x+40, main_center_y), main_center_color_x, 2)
            cv.line(overlay, (main_center_x, main_center_y-40), (main_center_x, main_center_y+40), main_center_color_y, 2)
            
            opacity = 0.7
            cv.addWeighted(overlay, opacity, cam, 1-opacity, 0, cam)    
            # img_blobs = cv.drawKeypoints(cam, keypoints, cam, (0,255,0), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            return cam
            # cv.imshow('pic', cam)

            # if cv.waitKey(1) & 0xFF==ord('q'):
            #     break 
        
    def parameters(self):
        #set up the detector with default parameters
        params = cv.SimpleBlobDetector_Params()

        #Defining threshold
        params.minThreshold = 0
        params.maxThreshold = 255
        
        #Filtering by area
        params.filterByArea = True
        params.minArea = 200
        params.maxArea = 1000

        #Filtering by color
        params.filterByColor = False
        # params.blobColor = 1

        #Filtering by circularity
        params.filterByCircularity = True
        params.minCircularity = 0.3
        params.maxCircularity = 1

        #detector object created after initializing the paramters
        detector = cv.SimpleBlobDetector_create(params)
        return detector

camera = 0
detect = Drill()

import cv2
import imageio
import shutil
import os
def MakeGIF(inputPNGs, outputFile):
    files_gif = []
    for file in inputPNGs:
        print(file)
        gif_each = imageio.imread(file)
        files_gif.append(gif_each)
    imageio.mimsave(outputFile, files_gif, "GIF", duration=0.03)

if __name__ == "__main__":
    face = cv2.VideoCapture("face.mp4")
    outputGIF = "face.gif"
    index = 0
    pngs = []
    while(face.isOpened()):
        ret,frame = face.read()
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        except:
            break
        frame = frame[100:700,:,:]
        # frame = []
        frame = cv2.resize(frame,(int(frame.shape[0]/4),int(frame.shape[1]/4)))
        # print(frame.shape)
        if index > 100 and index<250:
            # cv2.imshow('baby', frame)
            # print(index,index%3)
            # if index % 3.0 == 0:
            pngFile = str(index) + ".png"
            cv2.imwrite(pngFile,frame)
            pngs.append(pngFile)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
        index += 1
    face.release()
    cv2.destroyAllWindows()
    print(pngs)
    MakeGIF(pngs,outputGIF)
    # shutil.rmtree()
    os.system("rm -rf *.png")
import numpy as np
import cv2

#resmi belirtilen konumdan okuduk
img = cv2.imread('golgeli.jpeg')
#resim algılama işleminde kolaylık sağlaması için resmi gri yaptık
grayImg= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


#resmi gürültülerden arındırmak için gaussian filtresi uygulanarak resim blurlandı
smooth = cv2.GaussianBlur(grayImg, (95,95), 0)
cv2.imshow("smooth",smooth)
#gri resim ve filtre uygulanmış resme bölme işlemi uygulandı
division = cv2.divide(grayImg, smooth, scale=182)
#kenarları daha iyi algılamak için  division uygulanan görsele canny filtresi uygulandı
canny=cv2.Canny(division,600,600)
cv2.imshow("division",division)
#otsu threshold ile  otomatik eşik değerleri algılandı,division  resme uygulandı
ret , thresh = cv2.threshold(division,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

#canny filtresi uygulanmış görseldeki contour değerleri belirlendi
contours , hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# bulunan contour kısımları orjinal resimde çizildi
cv2.drawContours(img, contours, -1, (0, 0, 255), 1)
for c in contours:
    #sınırlayıcı dörtgenin sol üst  x,y koordinatları ,genişlik ve yüksekliğine değişken atanır
    x, y , w, h = cv2.boundingRect(c)
    #bulunan konturleri kapsayan dörtgenler  gri görselde çizilir
    grayImg = cv2.rectangle(grayImg,(x,y),(x+w,y+h),(0,255,0),2)

    cv2.imshow("Detected Shapes", grayImg)
    aspectRatio = float(w)/h
    area = cv2.contourArea(c)
    extent = area / float(w*h)
    perimeter = cv2.arcLength(c, True)    
    print(x)
    print(y)
    print(w)
    print(h)
    print(area)
    print(perimeter)

    if (abs((w*h) - area) < 1400):
       cv2.putText(img, "Square", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255))
       print("Square")
       print("-------------")

    elif (abs(((w*h) / 2) - area) <200):
       cv2.putText(img, "Triangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255))
       print("Triangle")
       print("-------------")
    
    elif (abs(((w*h) * 0.785) - area) <500):
       cv2.putText(img, "Circle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255))
       print("Circle")
       print("-------------")

    elif (abs(((w*h) * 0.738) - area) < 1000):
       cv2.putText(img, "Hexagon", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255))
       print("Hexagon")
       print("-------------")
    elif (abs(((w*h)*0.692))- area <1800):
       cv2.putText(img, "Pentagon", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255))
       print("Pentagon")
       print("-------------")

cv2.imshow('Shapes', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
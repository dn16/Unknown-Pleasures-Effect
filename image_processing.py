def contrastPoints(x,j,img):
    threshold=20
    contrast=[]
    i=0
    l2=1
    while l2==1:
        r1=img[i,j][0]
        b1=img[i,j][1]
        g1=img[i,j][2]
        ave1=((r1+b1+g1)/3)
        
        r2=img[(i+1),j][0]
        b2=img[(i+1),j][1]
        g2=img[(i+1),j][2]
        ave2=((r2+b2+g2)/3)

        r3=img[(i+2),j][0]
        b3=img[(i+2),j][1]
        g3=img[(i+2),j][2]
        ave3=((r3+b3+g3)/3)

        r4=img[(i+3),j][0]
        b4=img[(i+3),j][1]
        g4=img[(i+3),j][2]
        ave4=((r4+b4+g4)/3)

        if abs(ave2-ave1)>threshold:
            if abs(ave1-ave3)>(threshold/2):
                contrast.append(i)

        i=i+1		
        if i==(x-3):
            l2=0
    return contrast
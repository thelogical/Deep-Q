

def circleMatrix2(Cx,Cy,r):                                                #This function takes most of the time
    X = Cx - r
    Y = Cy - r
    TheMatrix = []
    for x in range(X,Cx+1):
        for y in range(Y,Cy+1):
            if( (x-Cx) * (x-Cx) + (y-Cy) * (y-Cy) <= r*r):
                xSym = Cx - (x - Cx)
                ySym = Cy - (y - Cy)
                TheMatrix.append((x, y))
                TheMatrix.append((x, ySym))
                TheMatrix.append((xSym, y))
                TheMatrix.append((xSym, ySym))
    return TheMatrix


def get_data(screen,pos,r):
    black = (0,0,0)
    white = (255,255,255)
    total = 0
    sand = 0
    matrix = circleMatrix2(pos[0],pos[1],r)
    for point in matrix:
        try:
            color = screen.get_at(point)[:-1]
            if color in [black, white]:
                if color == white:
                    sand += 1
                total+=1
        except IndexError:
            pass
    if total == 0:
        return 1
    return float(sand)/float(total)





def drawProgressBar(d, x, y, w, h, progress, bg="white", fg="green"):
    # draw background
    d.ellipse((x+w, y, x+h+w, y+h), fill=bg)
    d.ellipse((x, y, x+h, y+h), fill=bg)
    d.rectangle((x+(h/2), y, x+w+(h/2), y+h), fill=bg)

    # draw progress bar
    w *= progress
    d.ellipse((x+w, y, x+h+w, y+h), fill=fg)
    d.ellipse((x, y, x+h, y+h), fill=fg)
    d.rectangle((x+(h/2), y, x+w+(h/2), y+h), fill=fg)
    
    return d
BLUE_THRESHOLD_VALUE = 90
RED_THRESHOLD_VALUE = 50
GREEN_THRESHOLD_VALUE = 90

KERNEL_SIZE = 3
kernel = np.ones((KERNEL_SIZE, KERNEL_SIZE))

# Contour Analysis
MIN_SIZE = 600
MAX_SIZE = 4000

while True: 
    _, img = camera.read()
    if img is None:
        print(f"Unable to open camera {interface=}")
        break

    b_img = img[:,:,0]
    img_size = np.shape(b_img)
    _,b_imgt = cv2.threshold(b_img, BLUE_THRESHOLD_VALUE,255, cv2.THRESH_BINARY)
    #b_imgt = cv2.adaptiveThreshold(b_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5,2)
    b_imgt = cv2.dilate(cv2.erode(b_imgt,kernel),kernel)

    r_img = img[:,:,2]
    _,r_imgt = cv2.threshold(r_img, RED_THRESHOLD_VALUE,255, cv2.THRESH_BINARY)
    r_imgt = cv2.dilate(cv2.erode(r_imgt,kernel),kernel)

    g_img = img[:,:,1]
    _,g_imgt = cv2.threshold(r_img, GREEN_THRESHOLD_VALUE,255, cv2.THRESH_BINARY)
    g_imgt = cv2.dilate(cv2.erode(g_imgt,kernel),kernel)

    y_imgt = np.bitwise_and(g_imgt, r_imgt)
    m_imgt = np.bitwise_and(b_imgt, r_imgt)
    c_imgt = np.bitwise_and(b_imgt, g_imgt)

    thresh_filter = np.bitwise_xor.reduce([r_imgt, b_imgt, g_imgt, m_imgt, y_imgt, c_imgt])

    contours, hierarchy = cv2.findContours(thresh_filter, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)    

    key_image = cv2.cvtColor(np.zeros(img_size,dtype=np.uint8),cv2.COLOR_GRAY2BGR)
    contour_image = img
  
    cdb = np.hstack((
    np.vstack((
        cv2.putText(cv2.cvtColor(b_imgt,cv2.COLOR_GRAY2BGR), "Blue",(10,40),cv2.FONT_HERSHEY_PLAIN,2,(255,100,100),2),
        cv2.putText(cv2.cvtColor(r_imgt,cv2.COLOR_GRAY2BGR), "Red",(10,40),cv2.FONT_HERSHEY_PLAIN,2,(100,100,255),2),
        cv2.putText(cv2.cvtColor(g_imgt,cv2.COLOR_GRAY2BGR), "Green",(10,40),cv2.FONT_HERSHEY_PLAIN,2,(100,255,100),2),
    )),np.vstack((
        cv2.putText(cv2.cvtColor(y_imgt,cv2.COLOR_GRAY2BGR), "Yellow",(10,40),cv2.FONT_HERSHEY_PLAIN,2,(100,255,255),2),
        cv2.putText(cv2.cvtColor(m_imgt,cv2.COLOR_GRAY2BGR), "Magenta",(10,40),cv2.FONT_HERSHEY_PLAIN,2,(255,100,255),2),
        cv2.putText(cv2.cvtColor(m_imgt,cv2.COLOR_GRAY2BGR), "Cyan",(10,40),cv2.FONT_HERSHEY_PLAIN,2,(255,255,100),2),
    )),
    

      ))

    for i in range(len(contours)):       
        cv2.drawContours(contour_image, contours, i, (100,255,100),2, cv2.LINE_AA, hierarchy,0)
        cv2.drawContours(key_image, contours, i, (100,255,100),1, cv2.LINE_AA, hierarchy,0)

    hz = np.hstack((img,cv2.cvtColor(thresh_filter, cv2.COLOR_GRAY2BGR)))
    hz = np.vstack((hz,
    np.hstack((key_image,contour_image))
    ))

    cv2.imshow('New Im', hz)
    cv2.imshow('Debug',cdb)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
# del img, b_img, hzb, r_imgt, b_imgt, r_img, hz

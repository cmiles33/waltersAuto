import cv2
import pyscreenshot
from skimage.measure import compare_ssim


def imageSearch(pathto):
    # Full photo area
    pyscreenshot.grab().save('pictures/mygrab.png',format='png')
    img = cv2.imread('pictures/mygrab.png',0)
    img2 = img.copy()
    # Searching area
    template = cv2.imread(pathto,0)
    orginal = template
    w , h = template.shape[::-1]
    # Methods
    methods = ['cv2.TM_SQDIFF_NORMED']

    for meth in methods:
        img = img2.copy()
        mycrop = img.copy()
        method = eval(meth)
        res = cv2.matchTemplate(img, template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        print("Left Pixals")
        print(top_left[0])
        print(top_left[1])
        print("Right pixals")
        print(bottom_right[0])
        print(bottom_right[1])
        cv2.rectangle(img, top_left, bottom_right, 255, 2)

        #plt.subplot(121), plt.imshow(res, cmap='gray')
        #plt.title('Matching Result'), plt.xticks([]), plt.yticks([])

        # Plotting stuff
        # plt.subplot(122), plt.imshow(img, cmap='gray')
        # plt.title('Detected Point'), plt.xticks([]), plt.yticks([])

        mycrop = img[top_left[1]:top_left[1] + (bottom_right[1] - top_left[1]),
                 top_left[0]:top_left[0] + (bottom_right[0] - top_left[0])]
        #
        # plt.subplot(121), plt.imshow(mycrop, cmap='gray')

        # Find the match

        # Calculate Match Percentage
        (score, diff) = compare_ssim(mycrop,orginal,full=True)
        diff = (diff * 255).astype("uint8")
        print("SSIM: {}".format(score))
        print(" {}% Match".format(score*100))

        # plotting stuff
        # plt.title('Image that was found \n {}% Match'.format(score*100)), plt.xticks([]), plt.yticks([])
        # plt.suptitle(meth + "\n Looking for play all")
        # plt.show()
        # --------------

        xCord = top_left[1]
        print(xCord)
        x2Cord = bottom_right[1]
        print(x2Cord)
        length = x2Cord - xCord
        middle = xCord + length/2   # x Length
        print("Middle : {}".format(middle))
        print("y: {} ".format(bottom_right[0]))
        print("y: {} ".format(bottom_right[1]))
        yCord = top_left[0]
        y2Cord = bottom_right[0]
        length2 = yCord - y2Cord
        middle2 = yCord + length2
        print("x: {} y: {}".format(middle,middle2))
        returnValues = []
        if (score*100) > 50:
            # print("The image was found")
            returnValues.append("true")
            returnValues.append(int(top_left[0]+30))
            returnValues.append(int(bottom_right[1]-30))
            returnValues.append(score*100)
            # print(returnValues)
            return(returnValues)
        else:
            # print("Image not found")
            returnValues.append("false")
            returnValues.append(int(top_left[0]+30))
            returnValues.append(int(bottom_right[1]-30))
            returnValues.append(score * 100)
            # print(returnValues)
            return(returnValues)











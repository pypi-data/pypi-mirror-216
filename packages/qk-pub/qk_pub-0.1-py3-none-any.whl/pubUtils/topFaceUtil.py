import numpy as np

BUCKET_FACE_MIN = 1
BUCKET_FACE_MAX = 4
WORK_FACE_MIN = 1
WORK_FACE_MAX = 4

BUCKET_SLOT_WORK_FACE = np.array([[0, 0, 0, 0, 0],
                                  [0, 3, 4, 1, 2],
                                  [0, 2, 3, 4, 1],
                                  [0, 1, 2, 3, 4],
                                  [0, 4, 1, 2, 3]])


def getWorkDirection(bucketTopFace, workFace):
    bucketTopFace = int(bucketTopFace)
    workFace = int(workFace)
    if bucketTopFace < BUCKET_FACE_MIN or bucketTopFace > BUCKET_FACE_MAX:
        print("请检查bucketTopFace:{}".format(bucketTopFace))
        return bucketTopFace

    if workFace < WORK_FACE_MIN or workFace > WORK_FACE_MAX:
        print("workFace:{}".format(workFace))
        return bucketTopFace
    return BUCKET_SLOT_WORK_FACE[bucketTopFace, workFace]


if __name__ == '__main__':
    print(BUCKET_SLOT_WORK_FACE)
    print("\n")
    print(BUCKET_SLOT_WORK_FACE[[4], [1]])
    print(BUCKET_SLOT_WORK_FACE[4, 1])

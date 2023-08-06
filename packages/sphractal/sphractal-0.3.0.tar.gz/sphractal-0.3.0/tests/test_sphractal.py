from pytest import approx, fixture, mark
from sphractal.datasets import getExampleDataPath
from sphractal.utils import getMinMaxXYZ, readXYZ, findNN, findSurf, calcDist, closestSurfAtoms, oppositeInnerAtoms
from sphractal.surfPointClouds import fibonacciSphere, pointsOnAtom, pointsToVoxels
from sphractal.surfExact import getNearFarCoord, scanBox, writeBoxCoords, findTargetAtoms
from sphractal.boxCnt import getVoxelBoxCnt, getSphereBoxCnt, findSlope
from sphractal import runBoxCnt


@fixture
def exampleBoxCntDims():
    return (0.9967, 2.1778, (2.0038, 2.3517), 0.9971, 2.3454, (2.2183, 2.4725))


def test_getMinMaxXYZ():
    """Unit test of getMinMaxXYZ()."""
    atomsXYZ = 
    maxDimDiffTest, minXYZTest, maxXYZTest = getMinMaxXYZ(atomsXYZ)
    maxDimDiff, minXYZ, maxXYZ = 
    assert maxDimDiffTest == approx(maxDimDiff), "maxDimDiff incorrect!"
    assert minXYZTest == approx(minXYZ), "minXYZ incorrect!"
    assert maxXYZTest == approx(maxXYZ), "maxXYZ incorrect!"


def test_readXYZ():
    """Unit test of readXYZ()."""
    getExampleDataPath()
    atomsEle, atomsRad, atomsXYZ, maxDimDiff, minXYZ, maxXYZ = readXYZ(filePath)
    assert readXYZ()


@mark.parametrize('params', [(1.5, False), (1.2, True)])
def test_findNN(params):
    """Unit test of findNN()."""
    atomsNeighIdxsPadded, atomsAvgBondLen = findNN(atomsRad, atomsXYZ, minXYZ, maxXYZ, maxAtomRad, radMult, calcBL=False)

    assert


@mark.parametrize('params', ['alphaShape', 'convexHull', 'numNeigh'])
def test_findSurf(params):
    """Unit test of findSurf()."""
    expected = 
    actual = findSurf(atomsXYZ, atomsNeighIdxs, option=params, alpha=2.5)
    assert actual == expected, 'Incorrect surface atom indices'


def test_calcDist():
    """Unit test of calcDist()."""
    dTest = calcDist(p1, p2)
    assert dTest == approx(d)


def test_closestSurfAtoms():
    """Unit test of closestSurfAtoms()."""
    atomsXYZ[idxPair[0]], atomsXYZ[idxPair[1]] = closestSurfAtoms(pointXYZ, surfNeighIdxs, atomsXYZ, atomsNeighIdxs)
    assert


def test_oppositeInnerAtoms():
    """Unit test of oppositeInnerAtoms()."""
    isOppositeTest = oppositeInnerAtoms(pointXYZ, atom1XYZ, atomNeighIdxs, 
                                    atomsSurfIdxs, atomsXYZ, atomsNeighIdxs)
    assert isOppositeTest == True


def test_fibonacciSphere():
    """Unit test of fibonacciSphere()."""
    xyzsTest = fibonacciSphere(numPoint, sphereRad)
    assert


def test_pointsOnAtom():
    """Unit test of pointsOnAtom()."""
    outerSurfs, innerSurfs = pointsOnAtom(atomIdx, numPoint, atomsSurfIdxs, atomsRad, atomsXYZ, atomsNeighIdxs, surfPoints=None, rmInSurf=True)

    assert


def test_pointsToVoxels():
    """Unit test of pointsToVoxels()."""
    voxelXYZs, voxelIdxs = pointsToVoxels(pointXYZs, gridSize)

    assert


def test_getNearFarCoord():
    """Unit test of getNearFarCoord()."""
    scanBoxNear, scanBoxFar = getNearFarCoord(scanBoxIdx, scanBoxLen, lowBound, atomCoord)
    assert


def test_scanBox():
    """Unit test of scanBox()."""
    belongTest = scanBox(minXYZ, scanBoxIdxs, scanBoxNearFarXYZs, scanBoxLen,
                 atomIdx, atomRad, atomXYZ, atomNeighIdxs,
                 atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
                 rmInSurf=True):

    assert


def test_writeBoxCoords():
    """Unit test of writeBoxCoords()."""
    writeBoxCoords(atomsEle, atomsXYZ, allSurfBoxs, allBulkBoxs, minXYZ, scanBoxLens,
                   writeFileDir, npName)

    assert


def test_findTargetAtoms():
    """Unit test of findTargetAtoms()."""
    targetAtomsIdxsTest = findTargetAtoms(atomsNeighIdxs)

    assert


def test_findSlope():
    """Unit test of findSlope()."""
    r2PC, bcDimPC, confIntPC, r2ES, bcDimES, confIntES = findSlope(scaleChange, cntChange,
              writeFileDir, npName='', lenRange='Trimmed',
              visReg=False, saveFig=False, showPlot=False)
    assert


def test_getVoxelBoxCnt():
    """Integration test of getVoxelBoxCnts()."""
    scaleChange, cntChange = getVoxelBoxCnts(atomsEle, atomsRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
                    npName, writeFileDir='.', exeDir='.', procUnit='cpu', numPoint=300, gridNum=1024,
                    rmInSurf=True, vis=False, verbose=False, genPCD=False)
    assert


def test_getSphereBoxCnt():
    """Integration test of getSphereBoxCnts()."""
    scaleChange, cntChange = getSphereBoxCnts(atomsEle, atomsRad, atomsSurfIdxs, atomsXYZ, atomsNeighIdxs,
                     maxDimDiff, minMaxBoxLens, minXYZ, npName, writeFileDir='.',
                     rmInSurf=True, writeBox=False, verbose=False, boxLenConc=True, maxWorkers=2)
    assert 


def test_runBoxCnt(exampleBoxCntDims):
    """Integration test of runBoxCnt()."""
    runBoxCnt(xyzFilePath, findSurfOption='alphaShape', alphaMult=2.5, writeFileDir='.', lenRange='Trimmed',
              rmInSurf=True, vis=True, saveFig=True, showPlot=False, verbose=False,
              runPointCloudBoxCnt=True, numPoints=300, gridNum=1024, exeDir='.', procUnit='cpu', genPCD=False,
              runExactSphereBoxCnt=True, minLenMult=0.25, maxLenMult=1, writeBox=False, boxLenConc=True, maxWorkers=2)
    assert


def test_regression(exampleBoxCntDims):
    """Regression test for example.txt."""
    scaleChange, cntChange = runBoxCnt(getExampleDataPath())
    assert cntChange[0] == , 'First count has changed!'
    assert cntChange[-1] == , 'Last count has changed!'


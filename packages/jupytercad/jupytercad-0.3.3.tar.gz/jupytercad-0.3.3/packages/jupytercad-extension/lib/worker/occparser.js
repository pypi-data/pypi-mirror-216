export class OccParser {
    constructor(shapeList) {
        this._occ = self.occ;
        this._showEdge = true;
        this._shapeList = shapeList;
    }
    execute() {
        const maxDeviation = 0.1;
        const theejsData = {};
        this._shapeList.forEach(data => {
            const { shapeData, jcObject } = data;
            const { occShape, metadata } = shapeData;
            new this._occ.BRepMesh_IncrementalMesh_2(occShape, maxDeviation, false, maxDeviation * 5, true);
            const faceList = this._build_face_mesh(occShape);
            let edgeList = [];
            if (this._showEdge) {
                edgeList = this._build_edge_mesh(occShape);
            }
            const wireList = this._build_wire_mesh(occShape, maxDeviation);
            theejsData[jcObject.name] = {
                jcObject,
                faceList,
                edgeList: [...edgeList, ...wireList],
                meta: metadata
            };
        });
        return theejsData;
    }
    _build_wire_mesh(shape, maxDeviation) {
        const edgeList = [];
        const oc = this._occ;
        const expl = new oc.TopExp_Explorer_2(shape, oc.TopAbs_ShapeEnum.TopAbs_EDGE, oc.TopAbs_ShapeEnum.TopAbs_SHAPE);
        expl.Init(shape, oc.TopAbs_ShapeEnum.TopAbs_EDGE, oc.TopAbs_ShapeEnum.TopAbs_SHAPE);
        while (expl.More()) {
            const edge = oc.TopoDS.Edge_1(expl.Current());
            const aLocation = new oc.TopLoc_Location_1();
            const adaptorCurve = new oc.BRepAdaptor_Curve_2(edge);
            const tangDef = new oc.GCPnts_TangentialDeflection_2(adaptorCurve, maxDeviation, 0.1, 2, 1.0e-9, 1.0e-7);
            const vertexCoord = new Array(tangDef.NbPoints() * 3);
            for (let j = 0; j < tangDef.NbPoints(); j++) {
                const vertex = tangDef
                    .Value(j + 1)
                    .Transformed(aLocation.Transformation());
                vertexCoord[j * 3 + 0] = vertex.X();
                vertexCoord[j * 3 + 1] = vertex.Y();
                vertexCoord[j * 3 + 2] = vertex.Z();
            }
            edgeList.push({ vertexCoord, numberOfCoords: tangDef.NbPoints() * 3 });
            expl.Next();
        }
        return edgeList;
    }
    _build_face_mesh(shape) {
        const faceList = [];
        const triangulations = [];
        const oc = this._occ;
        const expl = new oc.TopExp_Explorer_2(shape, oc.TopAbs_ShapeEnum.TopAbs_FACE, oc.TopAbs_ShapeEnum.TopAbs_SHAPE);
        expl.Init(shape, oc.TopAbs_ShapeEnum.TopAbs_FACE, oc.TopAbs_ShapeEnum.TopAbs_SHAPE);
        while (expl.More()) {
            const face = oc.TopoDS.Face_1(expl.Current());
            const aLocation = new oc.TopLoc_Location_1();
            const myT = oc.BRep_Tool.Triangulation(face, aLocation);
            if (myT.IsNull()) {
                console.error('Encountered Null Face!');
                expl.Next();
                continue;
            }
            const thisFace = {
                vertexCoord: [],
                normalCoord: [],
                triIndexes: [],
                numberOfTriangles: 0
            };
            const pc = new oc.Poly_Connect_2(myT);
            const nodes = myT.get().Nodes();
            thisFace.vertexCoord = new Array(nodes.Length() * 3);
            for (let i = 0; i < nodes.Length(); i++) {
                const p = nodes.Value(i + 1).Transformed(aLocation.Transformation());
                thisFace.vertexCoord[i * 3 + 0] = p.X();
                thisFace.vertexCoord[i * 3 + 1] = p.Y();
                thisFace.vertexCoord[i * 3 + 2] = p.Z();
            }
            const orient = face.Orientation_1();
            // Write normal buffer
            const myNormal = new oc.TColgp_Array1OfDir_2(nodes.Lower(), nodes.Upper());
            // let SST = new oc.StdPrs_ToolTriangulatedShape();
            oc.StdPrs_ToolTriangulatedShape.Normal(face, pc, myNormal);
            thisFace.normalCoord = new Array(myNormal.Length() * 3);
            for (let i = 0; i < myNormal.Length(); i++) {
                const d = myNormal.Value(i + 1).Transformed(aLocation.Transformation());
                thisFace.normalCoord[i * 3 + 0] = d.X();
                thisFace.normalCoord[i * 3 + 1] = d.Y();
                thisFace.normalCoord[i * 3 + 2] = d.Z();
            }
            // Write triangle buffer
            const triangles = myT.get().Triangles();
            thisFace.triIndexes = new Array(triangles.Length() * 3);
            let validFaceTriCount = 0;
            for (let nt = 1; nt <= myT.get().NbTriangles(); nt++) {
                const t = triangles.Value(nt);
                let n1 = t.Value(1);
                let n2 = t.Value(2);
                const n3 = t.Value(3);
                if (orient !== oc.TopAbs_Orientation.TopAbs_FORWARD) {
                    const tmp = n1;
                    n1 = n2;
                    n2 = tmp;
                }
                thisFace.triIndexes[validFaceTriCount * 3 + 0] = n1 - 1;
                thisFace.triIndexes[validFaceTriCount * 3 + 1] = n2 - 1;
                thisFace.triIndexes[validFaceTriCount * 3 + 2] = n3 - 1;
                validFaceTriCount++;
            }
            thisFace.numberOfTriangles = validFaceTriCount;
            faceList.push(thisFace);
            triangulations.push(myT);
            expl.Next();
        }
        return faceList;
    }
    _build_edge_mesh(shape) {
        const oc = this._occ;
        const edgeList = [];
        const mapOfShape = new oc.TopTools_IndexedMapOfShape_1();
        oc.TopExp.MapShapes_1(shape, oc.TopAbs_ShapeEnum.TopAbs_EDGE, mapOfShape);
        const edgeMap = new oc.TopTools_IndexedDataMapOfShapeListOfShape_1();
        oc.TopExp.MapShapesAndAncestors(shape, oc.TopAbs_ShapeEnum.TopAbs_EDGE, oc.TopAbs_ShapeEnum.TopAbs_FACE, edgeMap);
        for (let iEdge = 1; iEdge <= edgeMap.Extent(); iEdge++) {
            const faceList = edgeMap.FindFromIndex(iEdge);
            if (faceList.Extent() === 0) {
                continue;
            }
            const anEdge = oc.TopoDS.Edge_1(mapOfShape.FindKey(iEdge));
            let myTransf = new oc.gp_Trsf_1();
            const aLoc = new oc.TopLoc_Location_1();
            const aPoly = oc.BRep_Tool.Polygon3D(anEdge, aLoc);
            const theEdge = {
                vertexCoord: [],
                numberOfCoords: 0
            };
            let nbNodesInFace;
            if (!aPoly.IsNull()) {
                if (!aLoc.IsIdentity()) {
                    myTransf = aLoc.Transformation();
                }
                nbNodesInFace = aPoly.get().NbNodes();
                theEdge.numberOfCoords = nbNodesInFace;
                theEdge.vertexCoord = new Array(nbNodesInFace * 3);
                const nodeListOfEdge = aPoly.get().Nodes();
                for (let ii = 0; ii < nbNodesInFace; ii++) {
                    const V = nodeListOfEdge.Value(ii + 1);
                    V.Transform(myTransf);
                    theEdge.vertexCoord[ii * 3 + 0] = V.X();
                    theEdge.vertexCoord[ii * 3 + 1] = V.Y();
                    theEdge.vertexCoord[ii * 3 + 2] = V.Z();
                }
            }
            else {
                const aFace = oc.TopoDS.Face_1(edgeMap.FindFromIndex(iEdge).First_1());
                const aPolyTria = oc.BRep_Tool.Triangulation(aFace, aLoc);
                if (!aLoc.IsIdentity()) {
                    myTransf = aLoc.Transformation();
                }
                const aPoly = oc.BRep_Tool.PolygonOnTriangulation_1(anEdge, aPolyTria, aLoc);
                if (aPoly.IsNull()) {
                    continue;
                }
                nbNodesInFace = aPoly.get().NbNodes();
                theEdge.numberOfCoords = nbNodesInFace;
                theEdge.vertexCoord = new Array(nbNodesInFace * 3);
                const indices = aPoly.get().Nodes();
                const nodeListOfFace = aPolyTria.get().Nodes();
                for (let jj = indices.Lower(); jj <= indices.Upper(); jj++) {
                    const v = nodeListOfFace.Value(indices.Value(jj));
                    v.Transform(myTransf);
                    const locIndex = jj - nodeListOfFace.Lower();
                    theEdge.vertexCoord[locIndex * 3 + 0] = v.X();
                    theEdge.vertexCoord[locIndex * 3 + 1] = v.Y();
                    theEdge.vertexCoord[locIndex * 3 + 2] = v.Z();
                }
            }
            edgeList.push(theEdge);
        }
        return edgeList;
    }
}

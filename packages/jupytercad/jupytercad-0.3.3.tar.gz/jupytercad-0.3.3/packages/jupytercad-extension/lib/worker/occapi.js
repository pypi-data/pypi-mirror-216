import { v4 as uuid } from 'uuid';
import { getOcc } from './actions';
import { _GeomCircle } from './geometry/geomCircle';
import { _GeomLine } from './geometry/geomLineSegment';
import { operatorCache } from './operatorcache';
import { toRad } from './utils';
function setShapePlacement(shape, placement) {
    if (!placement) {
        return shape;
    }
    const oc = getOcc();
    const trsf = new oc.gp_Trsf_1();
    const ax = new oc.gp_Ax1_2(new oc.gp_Pnt_3(0, 0, 0), new oc.gp_Dir_4(placement.Axis[0], placement.Axis[1], placement.Axis[2]));
    const angle = toRad(placement.Angle);
    trsf.SetRotation_1(ax, angle);
    trsf.SetTranslationPart(new oc.gp_Vec_4(placement.Position[0], placement.Position[1], placement.Position[2]));
    const loc = new oc.TopLoc_Location_2(trsf);
    shape.Location_2(loc);
    return shape;
}
function _Box(arg, _) {
    const { Length, Width, Height, Placement } = arg;
    const oc = getOcc();
    const box = new oc.BRepPrimAPI_MakeBox_2(Length, Width, Height);
    const shape = box.Shape();
    return setShapePlacement(shape, Placement);
}
function _Cylinder(arg, _) {
    const { Radius, Height, Angle, Placement } = arg;
    const oc = getOcc();
    const cylinder = new oc.BRepPrimAPI_MakeCylinder_2(Radius, Height, toRad(Angle));
    const shape = cylinder.Shape();
    return setShapePlacement(shape, Placement);
}
function _Sphere(arg, _) {
    const { Radius, Angle1, Angle2, Angle3, Placement } = arg;
    const oc = getOcc();
    const sphere = new oc.BRepPrimAPI_MakeSphere_4(Radius, toRad(Angle1), toRad(Angle2), toRad(Angle3));
    const shape = sphere.Shape();
    return setShapePlacement(shape, Placement);
}
function _Cone(arg, _) {
    const { Radius1, Radius2, Height, Angle, Placement } = arg;
    const oc = getOcc();
    const cone = new oc.BRepPrimAPI_MakeCone_2(Radius1, Radius2, Height, toRad(Angle));
    const shape = cone.Shape();
    return setShapePlacement(shape, Placement);
}
function _Torus(arg, _) {
    const { Radius1, Radius2, Angle1, Angle2, Angle3, Placement } = arg;
    const oc = getOcc();
    const torus = new oc.BRepPrimAPI_MakeTorus_4(Radius1, Radius2, toRad(Angle1), toRad(Angle2), toRad(Angle3));
    const shape = torus.Shape();
    return setShapePlacement(shape, Placement);
}
function _Cut(arg, content) {
    const { Placement, Base, Tool } = arg;
    const oc = getOcc();
    const baseObject = content.objects.filter(obj => obj.name === Base);
    const toolObject = content.objects.filter(obj => obj.name === Tool);
    if (baseObject.length === 0 || toolObject.length === 0) {
        return;
    }
    const baseShape = baseObject[0].shape;
    const toolShape = toolObject[0].shape;
    if (baseShape &&
        ShapesFactory[baseShape] &&
        toolShape &&
        ShapesFactory[toolShape]) {
        const base = ShapesFactory[baseShape](baseObject[0].parameters, content);
        const tool = ShapesFactory[toolShape](toolObject[0].parameters, content);
        if (base && tool) {
            baseObject[0].visible = false;
            toolObject[0].visible = false;
            const operator = new oc.BRepAlgoAPI_Cut_3(base.occShape, tool.occShape);
            if (operator.IsDone()) {
                return setShapePlacement(operator.Shape(), Placement);
            }
        }
    }
}
function _Fuse(arg, content) {
    const oc = getOcc();
    const { Shapes, Placement } = arg;
    const occShapes = [];
    Shapes.forEach(Base => {
        const baseObject = content.objects.filter(obj => obj.name === Base);
        if (baseObject.length === 0) {
            return;
        }
        const baseShape = baseObject[0].shape;
        if (baseShape && ShapesFactory[baseShape]) {
            const base = ShapesFactory[baseShape](baseObject[0].parameters, content);
            if (base) {
                occShapes.push(base.occShape);
                baseObject[0].visible = false;
            }
        }
    });
    const operator = new oc.BRepAlgoAPI_Fuse_3(occShapes[0], occShapes[1]);
    if (operator.IsDone()) {
        return setShapePlacement(operator.Shape(), Placement);
    }
    return;
}
function _Intersection(arg, content) {
    const oc = getOcc();
    const { Shapes, Placement } = arg;
    const occShapes = [];
    Shapes.forEach(Base => {
        const baseObject = content.objects.filter(obj => obj.name === Base);
        if (baseObject.length === 0) {
            return;
        }
        const baseShape = baseObject[0].shape;
        if (baseShape && ShapesFactory[baseShape]) {
            const base = ShapesFactory[baseShape](baseObject[0].parameters, content);
            if (base) {
                occShapes.push(base.occShape);
                baseObject[0].visible = false;
            }
        }
    });
    const operator = new oc.BRepAlgoAPI_Common_3(occShapes[0], occShapes[1]);
    if (operator.IsDone()) {
        return setShapePlacement(operator.Shape(), Placement);
    }
    return;
}
export function _SketchObject(arg, content) {
    const oc = getOcc();
    const builder = new oc.BRep_Builder();
    const compound = new oc.TopoDS_Compound();
    if (arg.Geometry.length === 0) {
        return undefined;
    }
    builder.MakeCompound(compound);
    for (const geom of arg.Geometry) {
        switch (geom.TypeId) {
            case 'Part::GeomCircle':
                builder.Add(compound, _GeomCircle(geom));
                break;
            case 'Part::GeomLineSegment': {
                builder.Add(compound, _GeomLine(geom));
                break;
            }
            default:
                break;
        }
    }
    return compound;
}
function _Extrude(arg, content) {
    const { Base, Dir, LengthFwd, LengthRev, Placement, Solid } = arg;
    const oc = getOcc();
    const baseObject = content.objects.filter(obj => obj.name === Base);
    if (baseObject.length === 0) {
        return;
    }
    const baseShape = baseObject[0].shape;
    if (baseShape && ShapesFactory[baseShape]) {
        const base = ShapesFactory[baseShape](baseObject[0].parameters, content);
        if (!base) {
            return;
        }
        const dirVec = new oc.gp_Vec_4(Dir[0], Dir[1], Dir[2]);
        const vec = dirVec.Multiplied(LengthFwd + LengthRev);
        let baseCopy = new oc.BRepBuilderAPI_Copy_2(base.occShape, true, false).Shape();
        if (LengthRev !== 0) {
            const mov = new oc.gp_Trsf_1();
            mov.SetTranslation_1(dirVec.Multiplied(-LengthRev));
            const loc = new oc.TopLoc_Location_2(mov);
            baseCopy.Move(loc);
        }
        if (Solid) {
            const xp = new oc.TopExp_Explorer_2(baseCopy, oc.TopAbs_ShapeEnum.TopAbs_FACE, oc.TopAbs_ShapeEnum.TopAbs_SHAPE);
            if (xp.More()) {
                //source shape has faces. Just extrude as-is.
            }
            else {
                const wireEx = new oc.TopExp_Explorer_2(baseCopy, oc.TopAbs_ShapeEnum.TopAbs_EDGE, oc.TopAbs_ShapeEnum.TopAbs_SHAPE);
                const wireMaker = new oc.BRepBuilderAPI_MakeWire_1();
                while (wireEx.More()) {
                    const ed = oc.TopoDS.Edge_1(wireEx.Current());
                    wireMaker.Add_1(ed);
                    wireEx.Next();
                }
                const wire = wireMaker.Wire();
                const faceMaker = new oc.BRepBuilderAPI_MakeFace_15(wire, false);
                baseCopy = faceMaker.Face();
            }
        }
        const result = new oc.BRepPrimAPI_MakePrism_1(baseCopy, vec, false, true);
        return setShapePlacement(result.Shape(), Placement);
    }
    return;
}
export function _Any(arg, content) {
    const { Shape, Placement } = arg;
    const result = _loadBrep({ content: Shape });
    if (result) {
        return setShapePlacement(result, Placement);
    }
}
export function _loadBrep(arg) {
    const oc = getOcc();
    const fakeFileName = `${uuid()}.brep`;
    oc.FS.createDataFile('/', fakeFileName, arg.content, true, true, true);
    const shape = new oc.TopoDS_Shape();
    const builder = new oc.BRep_Builder();
    const progress = new oc.Message_ProgressRange_1();
    oc.BRepTools.Read_2(shape, fakeFileName, builder, progress);
    oc.FS.unlink('/' + fakeFileName);
    return shape;
}
const Any = operatorCache('Part::Any', _Any);
const Box = operatorCache('Part::Box', _Box);
const Cylinder = operatorCache('Part::Cylinder', _Cylinder);
const Sphere = operatorCache('Part::Sphere', _Sphere);
const Cone = operatorCache('Part::Cone', _Cone);
const Torus = operatorCache('Part::Torus', _Torus);
const SketchObject = operatorCache('Sketcher::SketchObject', _SketchObject);
const Cut = operatorCache('Part::Cut', _Cut);
const Fuse = operatorCache('Part::MultiFuse', _Fuse);
const Intersection = operatorCache('Part::MultiCommon', _Intersection);
const Extrude = operatorCache('Part::Extrusion', _Extrude);
export const BrepFile = operatorCache('BrepFile', _loadBrep);
export const ShapesFactory = {
    'Part::Any': Any,
    'Part::Box': Box,
    'Part::Cylinder': Cylinder,
    'Part::Sphere': Sphere,
    'Part::Cone': Cone,
    'Part::Torus': Torus,
    'Part::Cut': Cut,
    'Part::MultiFuse': Fuse,
    'Part::Extrusion': Extrude,
    'Part::MultiCommon': Intersection,
    'Sketcher::SketchObject': SketchObject
};

import type { LiquidEtherProps, LiquidEtherWebGL } from "../types";

export const applyOptionsFromProps = (
    webgl: LiquidEtherWebGL | null, resolution: number, mouseForce: number,
    cursorSize: number, isViscous: boolean, viscous: number, iterationsPoisson: number, iterationsViscous: number,
    dt: number,
    BFECC: boolean,isBounce: boolean
) => {
    if (!webgl) return;
    const simulation = webgl.output?.simulation;
    if (!simulation) return;
    const prevRes = simulation.options.resolution;
    Object.assign(simulation.options, {
        mouse_force: mouseForce,
        cursor_size: cursorSize,
        isViscous,
        viscous,
        iterations_viscous: iterationsViscous,
        iterations_poisson: iterationsPoisson,
        dt,
        BFECC,
        resolution,
        isBounce
    });
    if (resolution !== prevRes) simulation.resize();
};
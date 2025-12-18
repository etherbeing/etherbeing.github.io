import React, { useEffect, useRef } from 'react';
import { defaultColors, type LiquidEtherProps, type LiquidEtherWebGL } from './types';
import { useWebGL } from './effects_hooks';

export default function LiquidEther({
    mouseForce = 20,
    cursorSize = 100,
    isViscous = false,
    viscous = 30,
    iterationsViscous = 32,
    iterationsPoisson = 32,
    dt = 0.014,
    BFECC = true,
    resolution = 0.5,
    isBounce = false,
    colors = defaultColors,
    style = {},
    className = '',
    autoDemo = true,
    autoSpeed = 0.5,
    autoIntensity = 2.2,
    takeoverDuration = 0.25,
    autoResumeDelay = 1000,
    autoRampDuration = 0.6
}: LiquidEtherProps): React.ReactElement {
    const mountRef = useRef<HTMLDivElement | null>(null);
    const webglRef = useRef<LiquidEtherWebGL | null>(null);

    useWebGL(
        mountRef,
        webglRef,
        colors,
        isViscous,
        isBounce,
        autoDemo,
        resolution,
        mouseForce,
        autoSpeed,
        viscous,
        iterationsPoisson,
        iterationsViscous,
        autoIntensity,
        cursorSize,
        takeoverDuration,
        autoResumeDelay,
        autoRampDuration,
        dt,
        BFECC
    )

    useEffect(() => {
        const webgl = webglRef.current;
        if (!webgl) return;
        const sim = webgl.output?.simulation;
        if (!sim) return;
        const prevRes = sim.options.resolution;
        Object.assign(sim.options, {
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
        if (webgl.autoDriver) {
            webgl.autoDriver.enabled = autoDemo;
            webgl.autoDriver.speed = autoSpeed;
            webgl.autoDriver.resumeDelay = autoResumeDelay;
            webgl.autoDriver.rampDurationMs = autoRampDuration * 1000;
            if (webgl.autoDriver.mouse) {
                webgl.autoDriver.mouse.autoIntensity = autoIntensity;
                webgl.autoDriver.mouse.takeoverDuration = takeoverDuration;
            }
        }
        if (resolution !== prevRes) sim.resize();
    }, [
        mouseForce,
        cursorSize,
        isViscous,
        viscous,
        iterationsViscous,
        iterationsPoisson,
        dt,
        BFECC,
        resolution,
        isBounce,
        autoDemo,
        autoSpeed,
        autoIntensity,
        takeoverDuration,
        autoResumeDelay,
        autoRampDuration
    ]);

    return (
        <div
            ref={mountRef}
            className={`w-full h-full relative overflow-hidden pointer-events-none touch-none ${className || ''}`}
            style={style}
        />
    );
}

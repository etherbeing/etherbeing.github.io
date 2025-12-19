import type { LiquidEtherWebGL } from "./types";
import { WebGLManager } from "./utils/classes";
import { applyOptionsFromProps } from "./utils/functions";
import { useEffect, useRef } from "react";

export function useWebGL(
    mountRef: React.RefObject<HTMLDivElement | null>,
    webglRef: React.RefObject<LiquidEtherWebGL | null>,
    colors: Array<string>,
    isViscous: boolean,
    isBounce: boolean,
    autoDemo: boolean,
    resolution: number,
    mouseForce: number,
    autoSpeed: number,
    viscous: number,
    iterationsPoisson: number,
    iterationsViscous: number,
    autoIntensity: number,
    cursorSize: number,
    takeoverDuration: number,
    autoResumeDelay: number,
    autoRampDuration: number,
    dt: number,
    BFECC: boolean
) {
    const resizeObserverRef = useRef<ResizeObserver | null>(null);
    const animationFrameRef = useRef<number | null>(null);
    const intersectionObserverRef = useRef<IntersectionObserver | null>(null);
    const isVisibleRef = useRef<boolean>(true);
    const resizeRafRef = useRef<number | null>(null);

    useEffect(() => {
        if (!mountRef.current) return;

        const container = mountRef.current;
        container.style.position = container.style.position || 'relative';
        container.style.overflow = container.style.overflow || 'hidden';

        const webgl = new WebGLManager({
            $wrapper: container,
            autoDemo,
            autoSpeed,
            autoIntensity,
            takeoverDuration,
            autoResumeDelay,
            autoRampDuration
        }, colors, isVisibleRef.current || false, animationFrameRef.current);
        
        webglRef.current = webgl;

        applyOptionsFromProps(webgl, resolution, mouseForce, cursorSize, isViscous, viscous, iterationsPoisson, iterationsViscous, dt, BFECC, isBounce);

        webgl.start();

        const io = new IntersectionObserver(
            entries => {
                const entry = entries[0];
                isVisibleRef.current = entry.isIntersecting && entry.intersectionRatio > 0;
                if (!webgl) return;
                if (isVisibleRef.current && !document.hidden) {
                    webgl.start()
                } else {
                    webgl.pause();
                }
            },
            { threshold: [0, 0.01, 0.1] }
        );
        io.observe(container);
        intersectionObserverRef.current = io;

        const ro = new ResizeObserver(() => {
            if (!webglRef.current) return;
            if (resizeRafRef.current) cancelAnimationFrame(resizeRafRef.current);
            resizeRafRef.current = requestAnimationFrame(() => {
                if (!webglRef.current) return;
                webglRef.current.resize();
            });
        });
        ro.observe(container);
        resizeObserverRef.current = ro;

        return () => {
            if (animationFrameRef.current) cancelAnimationFrame(animationFrameRef.current);
            if (resizeObserverRef.current) {
                try {
                    resizeObserverRef.current.disconnect();
                } catch {
                    /* noop */
                }
            }
            if (intersectionObserverRef.current) {
                try {
                    intersectionObserverRef.current.disconnect();
                } catch {
                    /* noop */
                }
            }
            if (webglRef.current) {
                webglRef.current.dispose();
            }
            webglRef.current = null;
        };
    }, [
        BFECC,
        cursorSize,
        dt,
        isBounce,
        isViscous,
        iterationsPoisson,
        iterationsViscous,
        mouseForce,
        resolution,
        viscous,
        colors,
        autoDemo,
        autoSpeed,
        autoIntensity,
        takeoverDuration,
        autoResumeDelay,
        autoRampDuration
    ])
}
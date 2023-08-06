import { LabIcon } from '@jupyterlab/ui-components';
export declare const jcLightIcon: LabIcon;
export declare const minimizeIcon: LabIcon;
export declare const boxIcon: LabIcon;
export declare const coneIcon: LabIcon;
export declare const sphereIcon: LabIcon;
export declare const cylinderIcon: LabIcon;
export declare const torusIcon: LabIcon;
export declare const cutIcon: LabIcon;
export declare const unionIcon: LabIcon;
export declare const intersectionIcon: LabIcon;
export declare const extrusionIcon: LabIcon;
export declare const axesIcon: LabIcon;
export declare const explodedViewIcon: LabIcon;
export declare const debounce: (func: CallableFunction, timeout?: number) => CallableFunction;
export declare function throttle<T extends (...args: any[]) => void>(callback: T, delay?: number): T;
export declare function itemFromName<T extends {
    name: string;
}>(name: string, arr: T[]): T | undefined;
export declare function focusInputField(filePath?: string, fieldId?: string | null, value?: any, color?: string, lastSelectedPropFieldId?: string): string | undefined;
export declare function getElementFromProperty(filePath?: string | null, prop?: string | null): HTMLElement | undefined | null;
export declare function removeStyleFromProperty(filePath: string | null | undefined, prop: string | null | undefined, properties: string[]): void;
export declare function nearest(n: number, tol: number): number;
export declare function getCSSVariableColor(name: string): string;
/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
export declare function requestAPI<T>(endPoint?: string, init?: RequestInit): Promise<T>;

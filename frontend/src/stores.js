/* /frontend/src/stores.js      */

import { writable } from 'svelte/store';

export const walletInstalled = writable(false);
export const walletInfo = writable();
export const txResults = writable();
export const userAccount = writable("");
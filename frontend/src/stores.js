/* /frontend/src/stores.js      */

import { writable } from 'svelte/store';

export const walletController = writable();
export const walletInstalled = writable(false);
export const walletInfo = writable();
export const userAccount = writable("");
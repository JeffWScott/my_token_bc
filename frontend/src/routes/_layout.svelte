<!-- /frontend/src/routes/_layout.svelte -->

<script>
	import Nav from '../components/Nav.svelte';
	import { onMount, setContext } from 'svelte'
	import WalletController from 'lamden_wallet_controller';
	import { walletInstalled, walletInfo, txResults } from '../stores'
	import { approvalRequest } from '../wallet_approval'

	let lwc;

	onMount(() => {
		lwc = new WalletController(approvalRequest)
		lwc.events.on('newInfo', handleWalletInfo)
		lwc.events.on('txStatus', handleTxResults)

		lwc.walletIsInstalled()
			.then(installed => {
				if (installed) walletInstalled.set('installed')
				else walletInstalled.set('not-installed')
			})

		return () => {
			lwc.events.removeListener(handleWalletInfo)
			lwc.events.removeListener(handleTxResults)
		}
	})

	setContext('app_functions', {
		sendTransaction: (transaction, callback) => lwc.sendTransaction(transaction, callback)
	})

	const handleWalletInfo = (info) => {
		console.log(info)
		if (!info.errors) walletInfo.set(info)
	}

	const handleTxResults = (results) => txResults.set(results)
</script>

<style>
	main {
		position: relative;
		max-width: 56em;
		padding: 2rem 28px 0;
		margin: 0 auto;
		box-sizing: border-box;
		display: flex;
		flex-direction: column;
		justify-content: center;
	}
</style>

<Nav />
<main>
	<slot></slot>
</main>

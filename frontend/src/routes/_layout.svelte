<script>
	import Nav from '../components/Nav.svelte';
	import { beforeUpdate, onDestroy, setContext } from 'svelte'
	import WalletController from 'lamden_wallet_controller';
	import { walletInstalled, walletInfo, txResults } from '../stores'
	import { approvalRequest } from '../wallet_approval'

	let lwc;

	setContext('app_functions', {
		sendTransaction: (transaction) => lwc.sendTransaction(transaction)
	})

	beforeUpdate(() => {
		if (!lwc) initializeLWC()
	})

	const initializeLWC = () => {
		lwc = new WalletController()
		lwc.events.on('newInfo', handleWalletInfo)
		lwc.events.on('txStatus', handleTxResults)

		lwc.walletIsInstalled()
			.then(installed => walletInstalled.set(installed))
	}

	onDestroy(() => {
		if (lwc) {
			lwc.events.removeListener(handleWalletInfo)
			lwc.events.removeListener(handleTxResults)
		}
	})

	const handleWalletInfo = (info) => {
		if (info.errors){
			if (info.errors[0].includes('lamdenWalletConnect')) lwc.sendConnection(approvalRequest)
		}else{
			walletInfo.set(info)
		}
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

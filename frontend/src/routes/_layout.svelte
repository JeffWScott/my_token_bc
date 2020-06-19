<script>
	import Nav from '../components/Nav.svelte';
	import { beforeUpdate } from 'svelte'
	import { goto } from '@sapper/app';
	import WalletController from 'lamden_wallet_controller';
	import { walletController, walletInstalled, walletInfo } from '../stores'
	import { approvalRequest } from '../wallet_approval'

	beforeUpdate(() => {
		if (!$walletController) getWalletController()
	})

	const getWalletController = () => {
		walletController.set(new WalletController())

		$walletController.walletIsInstalled()
				.then(installed => walletInstalled.set(installed))

		$walletController.events.on('newInfo', handleWalletInfo)
	}

	const handleWalletInfo = (info) => {
		if (info.errors){
			if (info.errors[0].includes('lamdenWalletConnect')) sendApprovalRequest()
		}else{
			walletInfo.set(info)
		}
	}

	const sendApprovalRequest = () => {
		$walletController.sendConnection(approvalRequest)
	}
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

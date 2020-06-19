<script>
	import {goto} from '@sapper/app';
	import {walletInstalled, walletInfo} from '../stores'
	import App from "../node_modules/@sapper/internal/App.svelte";

	$: account = $walletInfo ? $walletInfo.wallets[0] : undefined;
	$: locked = $walletInfo ? $walletInfo.locked : undefined;

	const login = () => {
		goto('/users/' + account);
	}

</script>

<style>
	*{
		text-align: center;
	}

	a, input {
		margin-top: 1rem;
	}
	.account{
		font-size: 0.9em;
		font-weight: 200;
		color: #161454;
	}
	.account > strong{
		font-weight: 400;
	}
	.lamden-logo{
		width: 50px;
		heigh: 50px;
	}
	.wallet-connected{
		display: flex;
		flex-direction: row;
		align-items: center;
		justify-content: center;
		font-weight: 800;
		font-size: 1.2em;
	}
	.wallet-connected > img {
		margin-right: 10px;
	}
	.connected{
    	border: 3px solid #00c100;
	}
	.locked{
		border: 3px solid #c71313;
	}
	.not-connected{
		background: #fff;
	}
</style>

<svelte:head>
	<title>My Token</title>
</svelte:head>

<div class="shadowbox"
     class:locked={$walletInfo ? $walletInfo.locked : false}
     class:connected={account}
     class:not-connected={!account && !locked}>
	{#if $walletInstalled}
		{#if $walletInfo.locked}
			<img class="lamden-logo" src="lamden_logo.png" alt="lamden logo" />
			<p>Please unlock the Lamden Wallet</p>
		{:else}
			<form on:submit|preventDefault={login}>
				<div class="wallet-connected">
					<img class="lamden-logo" src="lamden_logo.png" alt="lamden logo" />
					<p>Lamden Wallet Connected!</p>
				</div>
				<p class="account"><strong>Account Address: </strong>{account}</p>
				<input class="button" type="submit" value="sign in" />
			</form>
		{/if}
	{:else}
		<img src="wallet.png" alt="wallet" />
		<p>This site uses the Lamden Wallet browser extension for blockchain authentication.
			Please download and install it from the link below.</p>
		<a href="https://chrome.google.com/webstore/detail/lamden-wallet-browser-ext/fhfffofbcgbjjojdnpcfompojdjjhdim"
		   target="_blank"
		   rel="noopener noreferrer"
		   class="button">Download</a>
	{/if}
</div>


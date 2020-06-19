<script context="module">
	export async function preload({ params, query }) {
		const res = await this.fetch("http://167.172.126.5:18080/contracts/con_jeff_token/S?key=" + params.user)
		const data = await res.json();
		console.log(data)
		console.log(typeof data.value)
		console.log(data.value === null)
		if (typeof data.value === 'undefined') this.error(res.status, data.message);
		if (data.value === null) data.value = 0;
		return {value: data.value, user: params.user};
	}
</script>

<script>
	import { goto } from '@sapper/app';
	import { onMount, afterUpdate } from 'svelte'

	import { walletController, walletInfo, userAccount } from '../../stores'

	export let value;
	export let user;

	let receiver = "";
	let amount = 0;
	let walletUser = $walletInfo ? $walletInfo.wallets[0] : "";

	$: authenticatedUser = walletUser === user

	onMount(() => {
		$walletController.events.on('txStatus', handleTxResults)
		return () => {
			userAccount.set("")
			$walletController.events.removeListener(handleTxResults)
		}
	})

	afterUpdate(()=> {
		walletUser = $walletInfo ? $walletInfo.wallets[0] : "";
		userAccount.set(user)
	})

	const transfer = async () => {
		const transaction = {
			methodName: 'transfer',
			networkType: 'testnet',
			stampLimit: 50000,
			kwargs: {
				receiver,
				amount
			}
		}

		$walletController.sendTransaction(transaction)
	}

	const handleTxResults = (txResult) => {
		let status = txResult.data.txBlockResult.status
		if (status === 0) {
			alert("You sent " + amount + " token(s)!");
			refreshBalance();
			clearInputs();
		}else{
			if (typeof status !== 'undefined') {
				alert("There was an issue sending the tokens");
			}
		}
	}

	const refreshBalance = async () => {
		const res = await fetch("http://167.172.126.5:18080/contracts/con_jeff_token/S?key=" + user)
		const data = await res.json();
		value = data.value;
	}

	const clearInputs = () => {
		receiver = ""
		amount = 0
	}

	const logout = () => {
	    console.log('logging out')
		goto(`.`);
	}
</script>

<style>
	form{
		padding: 50px;
		color: #461BC2;
		margin: 1rem 0;
	}

	fieldset{
		display:flex;
		flex-direction: column;
		border: none;
	}

	input{
		width: 100%;
		margin-bottom: 1rem;
	}

	h1{
		text-transform: capitalize;
	}
	fieldset > h2{
		margin: 0 0 0.5em 0;
		font-weight: 800;
		line-height: 2.2;
		letter-spacing: 1px;
	}
	.balance{
		font-size: 1.2em;
		font-weight: 200;
	}
	.shadowbox{
		padding: 20px;
		max-width: 300px;
	}
	.shadowbox > p{
		margin: unset;
	}
	.token-logo{
		width: 50px;
	}
	.text-red{
		color: #ff8484;
	}

</style>

<svelte:head>
	<title>{"My Tokens"}</title>
</svelte:head>

<div class="shadowbox" >
	<img class="token-logo" src="wallet/icon.png" alt="token icon" />
	<p class="balance"><strong>Token Balance: </strong>{value}</p>
</div>

<form on:submit|preventDefault={transfer} >
	<fieldset disabled={!authenticatedUser}>
		<h2 class:text-red={!authenticatedUser}>
			{authenticatedUser
			 ? "Enter Transfer Details"
			 : "Please log in with the Lamden Wallet to enable transfers"}
		</h2>
		<label for="to">To</label>
		<input type="text" name="to" bind:value={receiver} required="true"/>
		<label for="amount">Token Amount</label>
		<input type="number" name="amount" bind:value={amount} required="true"/>
		<input class="button" type="submit" value="SEND"/>
	</fieldset>
</form>

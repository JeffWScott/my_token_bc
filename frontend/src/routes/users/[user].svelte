<!-- /frontend/src/routes/users/[user].svelte -->

<script context="module">
	let masternode = "https://testnet-master-1.lamden.io"

	export async function preload({ params, query }) {
		const res = await this.fetch(`${masternode}/contracts/con_jeff_token/S?key=${params.user}`)
		const data = await res.json();
		if (typeof data.value === 'undefined') this.error(res.status, data.message);
		if (data.value === null) data.value = 0;
		if (data.value.__fixed__) data.value = parseFloat(data.value.__fixed__)
		data.value = parseFloat(data.value);
		return {
			value: data.value,
			user: params.user
		};
	}
</script>

<script>
	import { afterUpdate, getContext } from 'svelte'
	import { walletInfo, userAccount, txResults } from '../../stores'
	import { fly, fade } from 'svelte/transition';
	import { quintOut, quintIn } from 'svelte/easing';

	export let value;
	export let user;

	let receiver = "";
	let amount = 0;
	let sending = false;
	let txResultMessage = ""
	let walletUser = $walletInfo.wallets ? $walletInfo.wallets[0] : "";

	const { sendTransaction } = getContext('app_functions')

	$: authenticatedUser = walletUser === user

	afterUpdate(()=> {
		walletUser = $walletInfo.wallets ? $walletInfo.wallets[0] : "";
		userAccount.set(user)
	})

	const transfer = async () => {
		const transaction = {
			methodName: 'transfer',
			networkType: 'testnet',
			stampLimit: 50,
			kwargs: {
				receiver,
				amount
			}
		}
		sending = true;
		txResultMessage = "... Sending Tokens ..."
		sendTransaction(transaction, doneSending)
		setTimeout(() => {
			txResultMessage = "There was a problem sending your transaction :(";
			sending = false
			clearInputs()
		}, 10000)
	}

	const doneSending = (result) => {
		console.log(result)
		let txResults = result.data
		if (!txResults.errors){
			if (txResults.txBlockResult.status === 0) {
				txResultMessage = "You sent " + amount + " token(s)!";
				refreshBalance();
				clearInputs();
			}
		}else{
			txResultMessage = "There was a problem sending your transaction :(";
		}
	}

	const refreshBalance = async () => {
		const res = await fetch(`${masternode}/contracts/con_jeff_token/S?key=${user}`)
		const data = await res.json();
		if (!data.value) value = 0
		if (data.value.__fixed__) value = parseFloat(data.value.__fixed__)
		value = parseFloat(data.value);
	}

	const clearInputs = () => {
		receiver = ""
		amount = 0
		txResults.set({})
		setTimeout(() => {
			sending = false;
			txResultMessage = ""
		}, 2000)
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
	fieldset > h2{
		margin: 0 0 0.5em 0;
		font-weight: 800;
		line-height: 2.2;
		letter-spacing: 1px;
	}
	p{
		text-align: center;
		font-size: 2em;
		margin: 4em;
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
{#if sending}
	<div in:fly="{{delay: 0, duration: 1000, x: -200, opacity: 0.0, easing: quintOut}}"
	     out:fly="{{delay: 0, duration: 300, x: 200, opacity: 0.0, easing: quintIn}}">
		<p>{txResultMessage}</p>
	</div>
{:else}
	<form on:submit|preventDefault={transfer}
		  in:fade="{{delay: 310, duration: 800,  opacity: 0.0, easing: quintOut}}">
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
{/if}

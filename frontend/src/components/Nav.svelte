<script>
	import { userAccount, txResults } from '../stores'
	import { beforeUpdate } from 'svelte'
	import { goto } from '@sapper/app';

	let tauAmount = 0;

	beforeUpdate(() => {
		if ($userAccount) refreshTAUBalance()
	})

	const refreshTAUBalance = async () => {
		const res = await fetch("http://167.172.126.5:18080/contracts/currency/balances?key=" + $userAccount)
		const data = await res.json();
		if (!data.value) tauAmount = 0
		else tauAmount = data.value;
	}

	const updateTau = (data) => {
		if (typeof data.txBlockResult.status !== 'undefined'){
			if (data.txBlockResult.status == 0) {
				if (status === 0) refreshTAUBalance();
			}
		}
	}

	txResults.subscribe(results => {
		if (results.data) updateTau(results.data)
	})

	const logout = () => {
		userAccount.set("")
		goto(`.`);
	}

</script>

<style>
	nav {
		padding: 0 2rem;
		display: flex;
		flex-direction: row;
		align-items: center;
		justify-content: space-between;
	}
	.brand{
		display: flex;
		flex-direction: row;
		align-items: center;
		font-weight: 300;
		font-size: 2em;
		width: -moz-fit-content;
		cursor: pointer;
	}
	.brand > img {
		width: 50px;
		min-width: 50px;
		margin-right: 8px;
	}
	.account{
		color: #161454;
		display: flex;
		flex-direction: column;
		align-items: flex-end;
		font-weight: 200;
		font-size: 1em;
		line-height: 1.2;
		text-align: right;
	}
	.account > div > p > strong {
		font-size: 1em;
	}
	.account > div {
		width: 50%;
		display: flex;
		flex-direction: row;
		justify-content: flex-end;
		align-items: center;
	}
	.address{
		width: 50%;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
		align-self: flex-end;
		margin: 0.5rem 0 0;
	}
	.dtau{
		color: #161454;
		margin-right: 10px;
	}
</style>

<nav>
	<div class="brand" on:click={logout}>
		<img alt='Token' src='token.png'>
		<p style={"min-width: -moz-fit-content;"}>My Token</p>
	</div>
	<div class="account">
		{#if $userAccount !== ""}
			<a href={`https://explorer.lamden.io/address/${$userAccount}`}
			   target="_blank"
			   rel="noopener noreferrer"
			   class="address">
				{$userAccount}
			</a>
			<div>
				<p class="dtau"><strong>dTAU: </strong> {tauAmount}</p>
				<button class="button-text" on:click={logout}>sign out </button>
			</div>
		{/if}
	</div>
</nav>
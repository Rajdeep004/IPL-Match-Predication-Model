<script setup>
const teams = [
	"Kolkata Knight Riders",
	"Rajasthan Royals",
	"Chennai Super Kings",
	"Delhi Capitals",
	"Mumbai Indians",
	"Sunrisers Hyderabad",
	"Royal Challengers Bangalore",
	"Kings XI Punjab",
]
const cities = [
	"Hyderabad",
	"Pune",
	"Indore",
	"Mumbai",
	"Kolkata",
	"Bangalore",
	"Delhi",
	"Chandigarh",
	"Kanpur",
	"Jaipur",
	"Chennai"
]
const team1 = ref("Select Batting Team");
const team2 = ref("Select Bowling Team");
const city = ref("Select City");
const runsLeft = ref();
const ballsLeft = ref();
const wickets = ref();
const totalRuns = ref();
const crr = ref();
const rrr = ref();
const isSameTeam = ref(false);
// if team1 is selected then team2 should not be same as team1
watchEffect(() => {
	if (team1.value === team2.value) {
		team2.value = "Select Bowling Team";
		isSameTeam.value = true;
	} else {
		isSameTeam.value = false;
	}
});
const winningTeam = ref("");
const handleSubmit = async () => {
	const options = {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ "batting_team": [team1.value], "bowling_team": [team2.value], "city": [city.value], "runs_left": [runsLeft.value], "balls_left": [ballsLeft.value], "wickets": [wickets.value], "total_runs_x": [totalRuns.value], "crr": [crr.value], "rrr": [rrr.value] })
	};

	await fetch('http://localhost:8000/predict', options)
		.then(response => response.json())
		.then(response => {
			console.log(response.predicted_winner[0]);
			winningTeam.value = response.predicted_winner[0];
		})
		.catch(err => console.error(err));
}
</script>

<template>
	<UContainer class="my-4 space-y-4">
		<h1 class="heading font-bold text-5xl sm:text-6xl md:text-7xl xl:text-8xl dark:text-white"> ML Based Predication
			of<span class="text-primary"> IPL Match</span> outcome.</h1>
		<form class="space-y-4" @submit.prevent="handleSubmit">
			<label class="text-lg font-bold">Enter Match Details</label>
			<USelectMenu v-model="team1" :options="teams" trailing-icon="i-heroicons-chevron-up-down-20-solid"
				required />
			<USelectMenu v-model="team2" :options="teams" trailing-icon="i-heroicons-chevron-up-down-20-solid"
				required />
			<span v-if="isSameTeam" class="text-red-400">Batting and Bowling Team can not be same</span>
			<USelectMenu v-model="city" :options="cities" trailing-icon="i-heroicons-chevron-up-down-20-solid"
				required />
			<UInput v-model="runsLeft" type="number" placeholder="Runs Left" required>
				<template #trailing>
					<span class="text-gray-500 dark:text-gray-400 text-xs">Runs</span>
				</template>
			</UInput>
			<UInput v-model="ballsLeft" type="number" placeholder="Balls Left" required><template #trailing>
					<span class="text-gray-500 dark:text-gray-400 text-xs">Balls</span>
				</template></UInput>
			<UInput v-model="wickets" type="number" placeholder="Wickets" required><template #trailing>
					<span class="text-gray-500 dark:text-gray-400 text-xs">Wickets Left</span>
				</template></UInput>
			<UInput v-model="totalRuns" type="number" placeholder="Target" required><template #trailing>
					<span class="text-gray-500 dark:text-gray-400 text-xs">Runs</span>
				</template> </UInput>
			<UInput v-model="crr" type="number" placeholder="Current Run Rate" required><template #trailing>
					<span class="text-gray-500 dark:text-gray-400 text-xs">crr</span>
				</template></UInput>
			<UInput v-model="rrr" type="number" placeholder="Required Run Rate" required><template #trailing>
					<span class="text-gray-500 dark:text-gray-400 text-xs">rrr</span>
				</template></UInput>
			<UButton type="submit" class="w-full bg-primary font-bold">Predict</UButton>
		</form>
		<h1 v-if="winningTeam !== ''" v-key="winningTeam"
			class="heading font-bold text-4xl md:text-5xl xl:text-6xl dark:text-white">
			Predicted winner is <br />
			<span class="text-primary">{{ winningTeam }}</span> 🎉
		</h1>

	</UContainer>
</template>

<style>
body {
	font-family: "Nunito", sans-serif;
	font-optical-sizing: auto;
	font-style: normal;
}

.heading {
	font-family: "Maven Pro", sans-serif;
	font-optical-sizing: auto;
	font-style: normal;
}
</style>
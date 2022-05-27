document.addEventListener('alpine:init', function () {
  Alpine.data('autocomplete', (path = '') => ({
    cities: [],
    citiesPath: path,

    async init(citiesPath) {
      const resp = await axios.get(this.citiesPath);
      this.replaceCities(resp);
    },

    trigger: {
      async ['@input.debounce'](event) {
        console.log('[', new Date().getTime(), ']', event.target.value);

        const resp = await axios.get(this.citiesPath, {
          params: {
            q: event.target.value,
          },
        });
        this.replaceCities(resp);
      },
    },

    replaceCities(response) {
      if (response.status !== 200) return;

      const { cities } = response.data;
      this.$data.cities.splice(0, this.$data.cities.length, ...cities);
    },
  }));
});

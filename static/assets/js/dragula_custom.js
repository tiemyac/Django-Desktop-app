
new Vue({
  el: '#list-studients',
  data: {
    items: []
  },
  mounted: function () {
        var that = this;
        setTimeout(function () {
            that.fetchItems("");
            that.selectYear();
        }, 1000);
  },
  methods: {
        fetchItems: function(year) {
            var trimestreSelected = $('#list-studients');
            var that = this;
            $.ajax({
                url: trimestreSelected.data('url'),
                method: 'get',
                data: {'year': year},
                success: function(response) {
                    that.items = response;
                },
            });
        },
        selectYear: function () {
        var that = this;
        var yearSelector = $('#selectYear');
        yearSelector.select2({
            placeholder: '-- Selectionnez le trimestre --',
        });
        yearSelector.on('select2:select', function (e) {
            that.fetchItems(e.params.data.id);
        });
    },
  }
});





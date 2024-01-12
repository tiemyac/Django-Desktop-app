
new Vue({
    el: "#noteComponent",
    data: {},
    methods: {
        viewNoteByStudient: function(e) {
            e.preventDefault();
            var btn = e.target.dataset;
            var studientId = btn.id;
            this.getNotesByStudient(studientId);
        },
        getNotesByStudient: function(studient) {
            var element = $("#noteComponent");
            $.ajax({
                url: element.data('url'),
                method: 'get',
                data: {pk: studient},
                success: function(res) {
                    //$("#noteModal").modal('show');
                    this.modalInit();
                }
            });
        },
        modalInit: function() {
            $('#noteModal').on('show.bs.modal', function(e) {
                alert("kit")
                //var modal = $(this);
                //modal.find('.modal-title').text(studient);
                //modal.find('.modal-body input.studient_id').val(studientId);
            });
        }
    }
});


YUI().use("datatable", function (Y) {

    // A table from data with keys that work fine as column names
    var simple = new Y.DataTable({
        columns: ["id", "name", "price"],
        data   : [
            { id: "ga_3475", name: "gadget",   price: "$6.99" },
            { id: "sp_9980", name: "sprocket", price: "$3.75" },
            { id: "wi_0650", name: "widget",   price: "$4.25" }
        ],
        summary: "Price sheet for inventory parts",
        caption: "Example table with simple columns"
    });

    simple.render("#simple");

    // Data with less user friendly field names
    var data = [
        {
            mfr_parts_database_id   : "ga_3475",
            mfr_parts_database_name : "gadget",
            mfr_parts_database_price: "$6.99"
        },
        {
            mfr_parts_database_id   : "sp_9980",
            mfr_parts_database_name : "sprocket",
            mfr_parts_database_price: "$3.75"
        },
        {
            mfr_parts_database_id   : "wi_0650",
            mfr_parts_database_name : "widget",
            mfr_parts_database_price: "$4.25"
        }
    ];

    var columnDef = [
        {
            key  : "mfr_parts_database_id",
            label: "Mfr Part ID",
            abbr : "ID"
        },
        {
            key  : "mfr_parts_database_name",
            label: "Mfr Part Name",
            abbr : "Name"
        },
        {
            key  : "mfr_parts_database_price",
            label: "Wholesale Price",
            abbr : "Price"
        }
    ];

    var withColumnLabels = new Y.DataTable({
        columns: columnDef,
        data   : data,
        summary: "Price sheet for inventory parts",
        caption: "These columns have labels and abbrs"
    }).render('#labels');

});

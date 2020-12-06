class Constraints {
    constructor(recallid) {
        this.recallid = recallid;
        this.i_try = 0;
        this.load(this);
        this.print();
    }

    load(that) {
        $.ajax({
            headers: { "X-CSRFToken": jQuery("[name=csrfmiddlewaretoken]").val() },
            type: 'GET',
            url: '/api/v1/constraint/' + this.recallid,
            success: function (result, status, xhr) {
                that.i_try++;
                that.json = result;
            },
            error: function (result, status, xhr) {
                that.i_try++;
                if (that.i_try <= 5) {
                    Toast.fire({
                        icon: 'error',
                        title: 'Fehler beim Laden der Beschränkungen',
                        text: 'Automatischer Retry in 5s.'
                    });
                    setTimeout(function () {
                        that.load(that);
                    }, 5000);
                }
                else {
                    Toast.fire({
                        icon: 'error',
                        title: 'Fehler beim Laden der Beschränkungen',
                        text: 'Maximale Anzahl der Versuche erreicht'
                    });
                }
            },
            timeout: 120000,
        });
    };

    change(index, field, changed_value) {
        this.json["data"][index][field] = changed_value;
    }

    save(callback){
        console.log(this.json);
        $.ajax({
            headers: { "X-CSRFToken": jQuery("[name=csrfmiddlewaretoken]").val() },
            type: 'PUT',
            data: JSON.stringify(this.json),
            dataType: "json",
            contentType: "application/json",
            url: '/api/v1/constraint/' + this.recallid,
            success: function (result, status, xhr) {
                Toast.fire({
                    icon: 'success',
                    title: 'Änderung gespeichert'
                }).then(function () {
                    window.location.reload();
                });
                if (callback) callback();
            },
            error: function (result, status, xhr) {
                Toast.fire({
                    icon: 'error',
                    title: 'Änderung konnte nicht gespeichert werden'
                });
            },
            timeout: 120000,
        });
    }

    reset() {
        this.load(this);
    }

    print() {
        console.log(this);
    }

    delete_group(index, group) {
        switch (group) {
            case 'fin':
                this.json["data"][index]['Constraint_Vehicle_VIN_FROM'] = null;
                this.json["data"][index]['Constraint_Vehicle_VIN_TO'] = null;
                break;
            case 'fleet':
                this.json["data"][index]['Constraint_Vehicle_EXTERNAL_ID_FROM'] = null;
                this.json["data"][index]['Constraint_Vehicle_EXTERNAL_ID_TO'] = null;
                break;
            case 'make':
                this.json["data"][index]['Constraint_Vehicle_MAKE'] = null;
                break;
            case 'model':
                this.json["data"][index]['Constraint_Vehicle_MODEL'] = null;
                break;
            case 'type':
                this.json["data"][index]['Constraint_Vehicle_TYPE'] = null;
                break;
            case 'series':
                this.json["data"][index]['Constraint_Vehicle_SERIES'] = null;
                break;
            case 'reg-date':
                this.json["data"][index]['Constraint_Vehicle_FIRST_REGISTRATION_DATE_FROM'] = null;
                this.json["data"][index]['Constraint_Vehicle_FIRST_REGISTRATION_DATE_TO'] = null;
                break;
            case 'odometer':
                this.json["data"][index]['Constraint_Vehicle_MILEAGE_FROM'] = null;
                this.json["data"][index]['Constraint_Vehicle_MILEAGE_TO'] = null;
                break;
            case 'user':
                this.json["data"][index]['Constraint_Vehicle_USER'] = null;
                break;
        }
    }
}
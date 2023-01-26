class PostData {

    alert_title = "Are you sure?";
    alert_message = "Are you sure you want to do it?";
    alert_submit_value = "Yes";
    success_message = "Done";
    swal_settings = {};
    settings = {};
    prePostTask() {
    }
    postSuccessSwalALert(response) {
        Swal.fire({
            title: this.success_message,
            text: `${JSON.stringify(response)}`,
            icon: 'success'
        });
    }
    postSuccessTask(response) {
        this.postSuccessSwalALert(response);
    }
    async post(url, data) {
        this.settings["url"] = url;
        this.settings["data"] = data;
        if (data instanceof FormData) {
            this.settings["processData"] = false;
            this.settings["contentType"] = false;
        }
        this.prePostTask();
        try {
            let response = await jQuery.post(this.settings);
            return response
        } catch (error) {
            this.postFailureTask(error);
        }
    }

    postWithSwal(url, data) {
        const default_swal_settings = {
            title: this.alert_title,
            text: this.alert_message,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: this.alert_submit_value,
            showLoaderOnConfirm: true,
            preConfirm: (val) => {
                if (val && this.swal_settings['inputAttributes']) {
                    const _key = this.swal_settings['inputAttributes']['name'];
                    if (_key) {
                        if (data instanceof FormData) {
                            data.append(_key, val);
                        } else {
                            data[_key] = val;
                        }
                    }
                }
                return this.post(url, data);
            }
        }
        Object.assign(default_swal_settings, this.swal_settings);
        Swal.fire(default_swal_settings).then((result) => {
            if (result.isConfirmed) {
                this.postSuccessTask(result.value);
            }
        });
    }
    postFailureTask(error) {
        //by default shows the error message
        Swal.showValidationMessage(
            `Request failed: ${error.responseText}`
        )
    }
}

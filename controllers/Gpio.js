const exec = require('child_process').exec;

class Gpio {
    
    constructor({ pin = 5, mode = 'out', ready = ()=>{} }){
        
        this.active = false;
        this.pin    = pin;
        this.mode   = mode;

        this.init().then(()=> { ready(); });
    }

    init(){
        return this.updateMode();
    }

    read(){
        return this.cmd(`gpio read ${this.pin}`)
            .then((state)=> {
                return state.replace(/[^\d]/gm,'');
            });
    }

    write(value){
        if (value === 1) {
            this.active = true;
        } else if (value === 0) {
            this.active = false;
        }
        
        return this.cmd(`gpio write ${this.pin} ${value}`);
    }

    cmd(command) {
        return new Promise((resolve, reject)=> {
            exec(command, (error, stdout, stderr) => {
                if (error) {
                    reject(error);
                }
                resolve(stdout);
            });
        });
    }

    getActie() {
        return this.active;
    }

    setActive(value) {
        this.active = value;
    }

    setPinMode(value) {
        if (value === "read" || value === "write") {
            this.mode = value;
            this.updateMode();
        } else {
            console.log("Invalid mode specified. Expected 'read' or 'write'");
        }
    }

    toggle() {
        if (this.active === true) {
            this.write(0);
            this.setActive(false);
        } else {
            this.write(1);
            this.setActive(true);
        }
    }

    updateMode() {
        return this.cmd(`gpio mode ${this.pin} ${this.mode}`);
    }
}

module.exports = Gpio;
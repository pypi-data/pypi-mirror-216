const AbstractHandler = require("./AbstractHandler")


class ArrayHandler extends AbstractHandler {
    process(command) {
        try {
            let processedArray = command.payload
            return processedArray
        } catch (error) {
            return this.process_stack_trace(error, this.constructor.name)
        }
    }
}

module.exports = new ArrayHandler()
cmd_option="${1}"
file_option="${2}"

# check if cmd option is empty
if [ -z "$cmd_option" ]
then
    echo "No command option provided."
    echo "Use -h or --help for usage."
    exit 1
fi

# show help
if [ "$cmd_option" = "-h" ] || [ "$cmd_option" = "--help" ]
then
    echo "Usage: docker_runner.sh [OPTION] [FILE]"
    echo "Run docker-compose files."
    echo ""
    echo "Options:"
    echo "  -d, --daemon                  Run docker-compose in daemon mode."
    echo "  -l, --logs                    Run docker-compose in logs mode."
    echo "  -s, --stop                    Stop docker-compose."
    echo "  -h, --help                    Show this help message."
    echo ""
    echo "Files:"
    echo "  elasticsearch   | elk          Run docker-compose-es.yml."
    exit 0
fi

# Check if file option is empty
if [ -z "$file_option" ]
then
    echo "No file option provided."
    echo "Use -h or --help for usage."
    exit 1
fi

# set file
if [ "$file_option" = "elasticsearch" ] || [ "$file_option" = "elk" ]
then
    file="docker-compose-es.yml"
else
    echo "Invalid file option: ${file_option}"
fi

# resolve relative path to absolute path
cd "$(dirname "$0")" || exit

# run docker-compose-{file}.yml
case ${cmd_option} in
    -d|--daemon)
        docker-compose -f "../docker/${file}" up -d
        ;;
    -l|--logs)
        docker-compose -f "../docker/${file}" logs
        ;;
    -s|--stop)
        docker-compose -f "../docker/${file}" down
        ;;
    *)
        echo "Invalid option: ${cmd_option}"
        echo "Use -h or --help for usage."
        exit 1
        ;;
esac
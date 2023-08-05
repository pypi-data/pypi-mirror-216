
#!/bin/bash

function usage {
  echo "Usage: $0 [options]"
  echo ""
  echo "Options:"
  echo "--help                   Display this help message and exit."
  echo ""
  echo "This script performs the following steps:"
  echo "1. Updates version number in setup.py"
  echo "2. Removes old distributions"
  echo "3. Builds new distribution"
  echo "4. Uploads new distribution to PyPI"
  echo "5. Uninstalls old version of the package"
  echo "6. Waits for the server to update to the latest version"
  echo "7. Clears pip cache"
  echo "8. Tries to install new version of the package"
}

# Check if --help option was provided
if [[ $1 == '--help' ]]; then
  usage
  exit 0
fi

# Update version number in setup.py
echo "Update version number in setup.py..."
python3 ./clear_clean_go_upgrage/renew_setup_version.py

echo "Removing old distributions..."
rm -rf ./dist/*

echo "Building new distribution..."
python3 setup.py sdist bdist_wheel

echo "Uploading new distribution to PyPI..."
twine upload dist/*

echo "Uninstalling old version of the package..."
pip3 uninstall -y kangforecast

# Increase the waiting time
WAIT_TIME=2

echo "Waiting for the server to update to the latest version... We set a 2 second break. Grab a cup of coffee and enjoy the view outside."
for ((i=0; i<$WAIT_TIME; i++)); do
  printf "\rWaiting... [%-2s] %d sec" $(printf '%0.s#' $(seq 1 $i)) $i
  sleep 1
done
printf "\n"

# Clear pip cache
echo "Clearing pip cache..."
pip3 cache purge

# Read the new version number
NEW_VERSION=$(cat new_version.txt)

# Try to install new version of the package
max_attempts=3
delay_between_attempts=3

attempt=0
until pip3 install --no-cache-dir kangforecast==$NEW_VERSION
do
    attempt=$((attempt + 1))

    if [ $attempt -ge $max_attempts ]
    then
        echo "Attempt limit reached. Please check your command or network status."
        exit 1
    fi

    echo "Installation failed, waiting ${delay_between_attempts} seconds before attempt number ${attempt}... In the meantime, grab a cup of coffee and enjoy the view."
    sleep $delay_between_attempts
done

echo "New version of the package successfully installed!"

echo "All done!"



# #!/bin/bash

# # Update version number in setup.py
# echo "Update version number in setup.py..."
# python3 ./clear_clean_go_upgrage/renew_setup_version.py

# echo "Removing old distributions..."
# rm -rf ./dist/*

# echo "Building new distribution..."
# python3 setup.py sdist bdist_wheel

# echo "Uploading new distribution to PyPI..."
# twine upload dist/*

# echo "Uninstalling old version of kangforecast..."
# pip3 uninstall -y kangforecast

# # Increase the waiting time
# WAIT_TIME=2

# echo "Waiting for the server to update to the latest version... We set a 2 second break. Grab a cup of coffee and enjoy the view outside."
# for ((i=0; i<$WAIT_TIME; i++)); do
#   printf "\rWaiting... [%-2s] %d sec" $(printf '%0.s#' $(seq 1 $i)) $i
#   sleep 1
# done
# printf "\n"

# # Clear pip cache
# echo "Clearing pip cache..."
# pip3 cache purge

# # Read the new version number
# NEW_VERSION=$(cat new_version.txt)

# # Try to install new version of kangforecast
# max_attempts=3
# delay_between_attempts=3

# attempt=0
# until pip3 install --no-cache-dir kangforecast==$NEW_VERSION
# do
#     attempt=$((attempt + 1))

#     if [ $attempt -ge $max_attempts ]
#     then
#         echo "Attempt limit reached. Please check your command or network status."
#         exit 1
#     fi

#     echo "Installation failed, waiting ${delay_between_attempts} seconds before attempt number ${attempt}... In the meantime, grab a cup of coffee and enjoy the view."
#     sleep $delay_between_attempts
# done

# echo "New version of kangforecast successfully installed!"

# echo "All done!"


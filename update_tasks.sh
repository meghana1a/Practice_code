#!/bin/bash

DB_NAME="migration_system"
COLLECTION_NAME="tasks"

# Connect to local MongoDB
mongosh $MONGO_URI --quiet <<EOF
// Find all tasks that are not completed
const tasks = db.$COLLECTION_NAME.find({ completed: false }).toArray();

if (tasks.length === 0) {
  print("No pending tasks found.");
} else {
  print("Updating the following tasks:\n");
  tasks.forEach(task => printjson(task));

  // Update tasks to in_progress
  const result = db.$COLLECTION_NAME.updateMany(
    { completed: false },
    { \$set: { in_progress: true } }
  );

  print("\nUpdated " + result.modifiedCount + " task(s).");
}
EOF

-- Create booklet table
CREATE TABLE IF NOT EXISTS booklet (
    id VARCHAR PRIMARY KEY,
    content TEXT NULL,
    results TEXT NULL
);

-- Create function to notify Kafka
CREATE OR REPLACE FUNCTION notify_kafka() RETURNS TRIGGER AS $$
DECLARE
    payload JSON;
BEGIN
    payload := json_build_object(
        'id', NEW.id,
        'content', NEW.content,
        'results', NEW.results
    );

    PERFORM pg_notify('kafka_topic', payload::TEXT);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to call the function on insert/update
CREATE TRIGGER trigger_notify
AFTER INSERT OR UPDATE ON booklet
FOR EACH ROW EXECUTE FUNCTION notify_kafka();

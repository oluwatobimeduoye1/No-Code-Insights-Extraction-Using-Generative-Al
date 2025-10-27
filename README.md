## No-Code Insights Extraction Using Amazon SageMaker Canvas and Amazon Kendra
This project demonstrates how to integrate Amazon SageMaker Canvas with Amazon Kendra to extract insights from company documents using Retrieval-Augmented Generation (RAG). The solution enables users to interact with their organizational data through a chat-based interface powered by large language models (LLMs) — without writing code.

# Overview
The solution uses Amazon SageMaker Canvas as a no-code interface for building and deploying generative AI-powered insights. Amazon Kendra serves as the intelligent search and retrieval engine, indexing organization documents stored in Amazon S3. When users query the system through SageMaker Canvas, the LLM accesses relevant snippets from Kendra’s index to generate accurate, contextually grounded responses all enabled by RAG

# Architecture
<img width="839" height="540" alt="Screenshot 2025-10-25 at 01 04 29" src="https://github.com/user-attachments/assets/c7f9678a-4154-47cd-9ba6-5cda9b013087" />
#### Workflow Summary:
- Documents (e.g., Amazon Shareholder Letters) are stored in an S3 bucket.

- An S3 event notification triggers a Lambda function whenever a new document is uploaded.

- The Lambda function invokes the StartDataSourceSyncJob API to update the Amazon Kendra index.

- Amazon Kendra indexes and retrieves relevant snippets for user queries.

- SageMaker Canvas uses an LLM (e.g., Llama-2-7b-Chat) to process user questions, referencing the Kendra-indexed content.

- The generated answer and citations are displayed to the user in SageMaker Canvas Chat Interface.


# Business Benefits  

### 1. Enhanced Knowledge Discovery  
- Enables non-technical teams to **extract insights** from large repositories (e.g., reports, policies, manuals) through natural-language queries.  
- Eliminates dependence on data scientists or ML engineers for document analysis.

### 2. Accelerated Decision-Making  
- Surfaces **relevant, context-aware insights** instantly from internal documents.  
- Improves productivity for knowledge workers across departments.

### 3. Cost and Time Efficiency  
- Built with **no-code AWS tools** — SageMaker Canvas and Kendra Developer Edition.  
- Automatically indexes new content via **S3 + Lambda event triggers**, reducing maintenance overhead.

### 4. Compliance and Auditability  
- Responses include **citations** to original document pages for transparency and traceability — ideal for regulated industries.

### 5. Low Technical Barrier  
- Empowers analysts, managers, and decision-makers to perform AI-driven document exploration without writing a single line of code.


# Setup 
### Step 1 – Create S3 Bucket
- Create a general-purpose S3 bucket (e.g., company-shareholder-letters-bucket).
- Upload all relevant organization files (e.g., “Amazon Shareholder Letters”).

### Step 2 – Configure S3 Event Notification
- Under S3 → Properties → Event Notifications, create a new notification.
- Set event type to PUT (Object Created).
- Set destination to invoke the Lambda function

### Step 3 – Create Lambda Function
Purpose: Automatically triggers Kendra data source sync when new documents are uploaded.
```
import boto3
import os

def lambda_handler(event, context):
    kendra = boto3.client('kendra')
    response = kendra.start_data_source_sync_job(
        Id=os.environ['KENDRA_DATA_SOURCE_ID'],
        IndexId=os.environ['KENDRA_INDEX_ID']
    )
    return response
```
- Environment Variables:

KENDRA_DATA_SOURCE_ID = <Your Data Source ID>

KENDRA_INDEX_ID = <Your Kendra Index ID>

### Step 4 – Create Amazon Kendra Index
- Navigate to Amazon Kendra → Indexes → Create index.
- Select Developer Edition (or GenAI Edition for enhanced generative AI capabilities).
- Create a dedicated IAM Role for Kendra with permissions to:

      i. Access the S3 bucket.
      ii. Write logs to CloudWatch.
      iii. Perform sync operations.

  <img width="1160" height="342" alt="Ni tees" src="https://github.com/user-attachments/assets/040602da-f1a1-41d0-892c-a8e9ff2e3e8c" />
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::company-shareholder-letters-bucket",
                "arn:aws:s3:::company-shareholder-letters-bucket/*"
            ],
            "Effect": "Allow"
        },
        {
            "Action": [
                "cloudwatch:PutMetricData",
                "logs:*"
            ],
            "Resource": "*",
            "Effect": "Allow"
        }
    ]
}
```
### step  5. Add additional capacity step, choose Developer edition.
The main difference between Amazon Kendra GenAl edition and Developer edition lies in their Al capabilities and pricing structure. While the Developer edition offers basic search functionality, the GenAl edition includes advanced generative Al features for more sophisticated query understanding and response generation, typically at a higher price point to reflect these enhanced capabilities.

### Step 6 – Add Data Source in Kendra

- In Kendra console, select Add data source → Amazon S3 connector.

- Define name and choose the IAM role created earlier.

- Browse to your S3 bucket and select it as the data source.

- Under Sync run schedule, select Run on demand.

- Start the sync process to index your documents.

#### During the sync process in Amazon Kendra, the service updates its index with the latest content from your connected data sources. This involves crawling the data sources, identifying new, modified, or deleted documents, and then updating the Kendra index accordingly to ensure that search results reflect the most current information available in your data repository 

### Step 7 – Configure Amazon SageMaker Canvas

#### These App Configurations allow you to customize the resources and settings for each application type, ensuring that users have the appropriate environment and computational power for their specific machine learning and data science tasks within the SageMaker Domain.

- Go to Amazon SageMaker → Domains.

- Under App Configurations → Canvas, enable:

 Enable document query using Amazon Kendra

- Choose your Kendra index.

- In Amazon Bedrock Role Section, select the IAM role with Bedrock access.

- Click Submit

#### Amazon SageMaker Canvas is a no-code ML service. SageMaker Canvas supports the entire ML workflow, including data preparation, model building and training, generating predictions, and deploying the models to production. With SageMaker Canvas, you can use ML to detect fraud, predict maintenance failures, forecast financial metrics and sales, optimize inventory, generate content, and more.



### Step 8 – Deploy the Foundation Model

- Open SageMaker Canvas → Navigate to Gen AI → Query Documents.

- Under SageMaker JumpStart Models, select Llama-2-7b-Chat.

- Click Deploy to make the model available in your workspace.



### Step 9 – Test the Solution

In SageMaker Canvas, start a new chat.

Enter questions like:

“What are the major amazon investment in 2021?”




<img width="1411" height="821" alt="Screenshot 2025-10-25 at 00 45 30" src="https://github.com/user-attachments/assets/57a9699a-d6b7-4bef-83a0-cd5e12f749bd" />




# Outcome

- Deploy Amazon Kendra as a searchable document knowledge base.

- Integrate SageMaker Canvas for no-code LLM-driven querying.

- Enable RAG-based generative responses grounded in corporate documents.

- Gain hands-on experience in no-code AI integration across AWS services.

























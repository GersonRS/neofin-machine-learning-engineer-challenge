{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "magalu-machine-learning-engineer-challenge.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/* Create chart name and version to be used by the chart label */}}
{{- define "magalu-machine-learning-engineer-challenge.chart" }}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{ end -}}

{{/* Define selectors to be used (to be also used as templates) */}}
{{- define "magalu-machine-learning-engineer-challenge.selector" }}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{ end -}}

{{/* Define common labels */}}
{{- define "magalu-machine-learning-engineer-challenge.labels" -}}
{{ include "magalu-machine-learning-engineer-challenge.selector" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{ end -}}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ include "magalu-machine-learning-engineer-challenge.chart" . }}
{{- end -}}
{{/* End labels */}}


{{/*
Create the name of the deployment service account to use
*/}}
{{- define "magalu-machine-learning-engineer-challenge.serviceAccountName" -}}
{{- if .Values.deployment.serviceAccount.create }}
{{- default (printf "%s-deployment" (include "magalu-machine-learning-engineer-challenge.fullname" .)) .Values.deployment.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.deployment.serviceAccount.name }}
{{- end }}
{{- end }}


{{/* User defined deployment environment variables */}}
{{- define "custom_deployment_environment" }}
  # Dynamically created environment variables
  {{- range $i, $config := .Values.env }}
  - name: {{ $config.name }}
    value: {{ $config.value | quote }}
  {{- end }}
  # Dynamically created secret envs
  {{- range $i, $config := .Values.secret }}
  - name: {{ $config.envName }}
    valueFrom:
      secretKeyRef:
        name: {{ $config.secretName }}
        key: {{ default "value" $config.secretKey }}
  {{- end }}
  # Extra env
  {{- $Global := . }}
  {{- with .Values.extraEnv }}
    {{- tpl . $Global | nindent 2 }}
  {{- end }}
{{- end }}
